from typing import Optional, List, TypedDict
from langgraph.graph import END, StateGraph  # not sure about the from langgraph import stuff 
from langgraph.graph.graph import CompiledGraph
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables  import RunnableConfig
from langchain.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from firebase_functions.params import StringParam
from base_chains import ChatGroqSingleton
from examples import create_shot_prompt, activate_shot_prompt, time_shot_prompt

TASK_DESCRIPTION = "create task description"
DURATION = "determine duration"
ACTIVE = "determine if task should be active"

class TaskState(TypedDict, total=False):
    input: List[tuple]
    description: Optional[str]
    duration: Optional[int]
    active: Optional[bool]

class Description(BaseModel):
    description: str = Field(..., description="concise but specific summary of the task the user wants to complete")

class Activate(BaseModel):
    activate_task: str = Field(description= "binary 'yes' or 'no' decsion whether or not to activate a task")
    confidence: float = Field(description= "confidence in the decision")
    reasoning: str = Field(description= "reasoning behind the decision")

class Duration(BaseModel):
    duration: int = Field(description="The estimated time needed to complete the task in minutes")

def task_description(state: TaskState, config: RunnableConfig):
    """Create a task that the user will try to complete within a couple of minutes."""
    print("CREATE TASK DESCRIPTION")
    parser = JsonOutputParser(pydantic_object=Description)
        
    task_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert in identifying the task.
                You will be provided with the recent messages between the user and the AI assistant. Respond by summarizing the 
                task in a very concise and clear way that excludes specific details.\n
                The users most recent response is the most important while all other messages from the user and the ai should just be used for context.
                In case there is no clear immediate task that has been agreed upon then set task to none.\n
                The response should be in the form of a JSON object with the keys 'description'
                
                the content of the message should ONLY include the JSON object. Do not include any additional text in the response.
                """,
            ),
            create_shot_prompt,
            MessagesPlaceholder("input")
        ]
    )

    model = ChatGroqSingleton().get_llm()
    chain = task_template | model | parser
    result = chain.invoke({"input" : state["input"]})
    print(f"CREATE_TASK result: {result}")

    if result:
        return {"description": result["description"]}
    else:
        return None
    
def activate_task(state: TaskState, config: RunnableConfig) -> str:
    print("ACTIVATE TASK")
    parser = JsonOutputParser(pydantic_object=Activate)

    ACTIVATE_TASK_CONDITIONAL_PROMPT = ChatPromptTemplate.from_messages(
        [
            activate_shot_prompt,
            (
                "system",
                """
                You are an expert conversation analyst tasked with determining if a given task has been sufficiently broken down and is ready for immediate action.

                Analyze the entire conversation history provided to understand the context of the task.

                Evaluate the task against the following criteria:
                1. Specificity: Is the task clearly defined with no ambiguity?
                2. Immediacy: Can the user start working on this task right away?
                3. Timeframe: Can the task be completed in a short amount of time (ideally within an hour)?
                4. Simplicity: Does the task require no further planning or decision-making?
                5. Focus: Is this a single, focused action rather than a multi-step process?

                If the task meets all or most of these criteria, it should be activated. If it fails to meet multiple criteria, it should not be activated.

                Common reasons NOT to activate a task include:
                - The task is too broad or the goal is unclear
                - The user is still working out details or planning
                - The task requires significant time or resources to complete
                - The task can be broken down further into simpler steps
                - The task requires additional information or resources before it can be started

                Be extra critical when evaluating as only the most simple and actionable tasks should be activated.

                Based on your analysis, provide a JSON response with the following structure:

                activate_task: <"yes" or "no">,
                confidence: <a number between 0 and 1>,
                reasoning: <A brief explanation of your decision>


                Only include this JSON object in your response, with no additional text.
                """
            ),
            ("system", "Here is the conversation between the user and the assistant: {input}"),
            ("system", "task created: {task}\n should task be activated?")
        ]
    )
    model = ChatGroqSingleton().get_llm()
    chain = ACTIVATE_TASK_CONDITIONAL_PROMPT | model | parser
    result = chain.invoke({"input": state["input"], "task": state["description"]}, config)
    print(f"ACTIVATE_TASK result: {result}")
    if not isinstance(result, dict):
        raise ValueError("Invalid result from model. Expected AIMessage.")
    
    if result["activate_task"] == "yes":
        return {"active": True}
    else:
        return {"active": False}
    

# def duration_or_end(state: TaskState) -> str:
#     print("TIME CONDITIONAL EDGE")
#     if state["active"] is True:
#         print("going into duration node")
#         return DURATION
#     else:
#         print("heading back out")
#         state["duration"] = 0
#         return END
    
def set_duration(state: TaskState, config: RunnableConfig) -> str:
    print("we are at time duration")
    parser = JsonOutputParser(pydantic_object=Duration)

    TIME_TASK_CONDITIONAL_PROMPT = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert at determining the duration of the tasks given. 
                If a task has been determined as an activated task, then Respond by giving the user
                the estimated time taken to complete the task. 

                The response must be in the form of a JSON object with the key 'duration'.
                The value should be an integer that is in minutes and within a 60 minute time frame.

                the content of the message should ONLY include the JSON object. Do not include any additional text in the response.
                """
            ),
            time_shot_prompt,
            MessagesPlaceholder("input"),
        ]
    )

    model = ChatGroqSingleton().get_llm()
    chain = TIME_TASK_CONDITIONAL_PROMPT | model | parser
    result = chain.invoke({"input": state["input"], "task": state["description"]}, config)
    print(f"TIME_TASK result: {result}")

    if not isinstance(result, dict):
        raise ValueError("Invalid result from model. Expected AIMessage.")
    
    if result["duration"] <= 60 and result["duration"] > 0:
        return {"duration": result["duration"]}
    return {"duration": 0}

def create_task() -> CompiledGraph:
    print("We are in create graph")

    workflow = StateGraph(TaskState)

    workflow.add_node(TASK_DESCRIPTION, task_description)
    workflow.add_node(DURATION, set_duration)
    workflow.add_node(ACTIVE, activate_task)
    workflow.add_edge(TASK_DESCRIPTION, DURATION)
    workflow.add_edge(DURATION, ACTIVE)
    workflow.set_entry_point(TASK_DESCRIPTION)
    workflow.set_finish_point(ACTIVE)

    graph = workflow.compile()
    return graph