from typing import List, Optional, TypedDict
from langgraph.graph import END, StateGraph  # not sure about the from langgraph import stuff 
from langgraph.graph.graph import CompiledGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables  import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from base_chains import ChatGroqSingleton
from create_task import create_task
from examples import model_shot_prompt, activate_shot_prompt, time_shot_prompt


ASSIGN_TOOLS = "Assigning the tools"
RESPONSE = "Producing the response"
TASK_CALL_CONDITIONAL = "Decide if we want to create a task"
ACTIVATE_TASK_CONDITIONAL = "Decide if we want to activate a task"
TIME_TASK_CONDITIONAL = "Determine if the task is activated"

class GenerativeUIState(TypedDict, total=False):
    input: List[tuple]
    tasks: List[str]
    result: Optional[str]
    # parsed tool calls
    tool_calls: Optional[set]
    # result of the tool calls
    tool_results: Optional[dict]

class DecideTaskCreation(BaseModel):
    create_task: str = Field(description= "decide whether or not to create a task")
class ActivateTask(BaseModel):
    activate_task: str = Field(description= "binary 'yes' or 'no' decsion whether or not to activate a task")
    confidence: float = Field(description= "confidence in the decision")
    reasoning: str = Field(description= "reasoning behind the decision")

class TimeTaskCreation(BaseModel):
    time_task: int = Field(description="The estimated time needed to complete the task in minutes")

def create_task_conditional(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
    print("CREATE TASK")
    parser = JsonOutputParser(pydantic_object=DecideTaskCreation)

    CREATE_TASK_CONDITIONAL_PROMPT = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert conversation analyst. 
                decide if the user is trying to pursue a specific task.

                If any of the below conditions are met do NOT call create_task tool:
                - user is not trying to pursue a specific task
                - user is working out the details of current task
                - if the determined task is the same as a task within the "task history" (Note: sub-tasks are considered different)

                here is the "task history": {tasks}

                The response should be in the form of a JSON object with the keys 'create_task'.
                The value should be a binary score 'yes' or 'no' indicating whether or not to call the create_task tool.

                the content of the message should ONLY include the JSON object. Do not include any additional text in the response.

                Below is the "conversation history" will be provided:
                """
            ),
            model_shot_prompt,
            MessagesPlaceholder("input")
        ]
    )
    model = ChatGroqSingleton().get_llm()
    chain = CREATE_TASK_CONDITIONAL_PROMPT | model | parser
    result = chain.invoke({"input": state["input"], "tasks": state["tasks"]}, config)
    print(f"INVOKE TOOL result: {result}, type is {type(result)}")
    if not isinstance(result, dict):
        raise ValueError("Invalid result from model. Expected AIMessage.")
    
    if result["create_task"] == "yes":
        return {"tool_calls": {"create_task"}}

def invoke_tools(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
    print(f"INVOKE TOOLS: {state['tool_calls']}")

    tool_results = []
    tools_map = {
        "create_task": create_task
    }

    if state["tool_calls"] is None:
        return
    
    print(f"pre tool call itteration")
    for tool_call in state["tool_calls"]:
        print(f"inside the loop: {tool_call}")
        print(f"inside the loop state['input'] type is: {type(state['input'])}")
        selected_tool = tools_map[tool_call]
        tool_results.append(selected_tool.invoke({"input":state["input"]}))
    print(f"TOOL RESULTS from invoke: {tool_results}")
    return {"tool_results": {tool_call: tool_results[0].description}, "tasks": state["tasks"] + [tool_results[0].description]}

def activate_task_or_respond(state: GenerativeUIState) -> str:
    print(f"TASK LIST: {state['tasks']}, typing: {type(state['tasks'])}")
    print("CONDITIONAL EDGE")
    if "tool_calls" in state and isinstance(state["tool_calls"], set):
        return ACTIVATE_TASK_CONDITIONAL
    else:
        return RESPONSE
    
def activate_task(state: GenerativeUIState, config: RunnableConfig) -> str:
    print("ACTIVATE TASK")
    parser = JsonOutputParser(pydantic_object=ActivateTask)

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
    result = chain.invoke({"input": state["input"], "task": state["tasks"][-1]}, config)
    print(f"ACTIVATE_TASK result: {result}")
    if not isinstance(result, dict):
        raise ValueError("Invalid result from model. Expected AIMessage.")
    
    if result["activate_task"] == "yes":
        return {"tool_calls": {"activate_task"}}
    print(f"no tool call made: {result}")

def time_task_or_respond(state: GenerativeUIState) -> str:
    print("TIME CONDITIONAL EDGE")
    if state["tool_calls"] and "activate_task" in state["tool_calls"]:
        return TIME_TASK_CONDITIONAL
    else:
        return RESPONSE
    
def time_duration(state: GenerativeUIState, config: RunnableConfig) -> str:
    print("we are at time duration")
    parser = JsonOutputParser(pydantic_object=TimeTaskCreation)

    TIME_TASK_CONDITIONAL_PROMPT = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert at determining the duration of the tasks given. 
                If a task has been determined as an activated task, then Respond by giving the user
                the estimated time taken to complete the task. 

                The response must be in the form of a JSON object with the key 'time'.
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
    result = chain.invoke({"input": state["input"], "task": state["tasks"][-1]}, config)
    print(f"TIME_TASK result: {result}")

    if not isinstance(result, dict):
        raise ValueError("Invalid result from model. Expected AIMessage.")
    
    if result["time"] <= 60 and  result["time"] > 0:
        return {"tool_calls": {"time"}}
    print(f"no tool call made: {result}")

def produce_response(state: GenerativeUIState, config: RunnableConfig) -> str:
    print("we are at the produce response")

    if state["tool_calls"] and "activate_task" in state["tool_calls"]:
        print("inside the if statement")
        state["input"].append(("system", f"prompt the user to commit to the task: {state['tasks'][-1]}"))
        print(f"CHECK if activate task is appeneded: {state['input']}")

    RESPONSE_PROMPT = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that guides users in breaking down tasks.\
                 You make users feel heard while prompting them to think about their\
                 task and how it can be reduced or if they have already made progress\
                 towards said task. Keep reducing tasks until they can be completed\
                 within a couple of minutes. Make the user feel as little overwhelmed\
                 as possible. Ask one thing at a time to help pin point a first task\
                 that can be completed. Be concise."
            ),   
        ] + state["input"]
    )
    model = ChatGroqSingleton().get_llm()
    chain = RESPONSE_PROMPT | model | StrOutputParser()
    result = chain.invoke(config)
    print("we are at the end of produce response")
    return {"input" : [("assistant", result)] }


def create_graph() -> CompiledGraph:
    print("We are in create graph")

    workflow = StateGraph(GenerativeUIState)

    # workflow.add_node(MODEL_CALL, invoke_model) # This part calls the AI and it will decide what to respond with
    # workflow.add_node(ASSIGN_TOOLS, invoke_tools) # This basically assigns and calls the tools that the AI is assigned to or return plain text
    workflow.add_node(TASK_CALL_CONDITIONAL, create_task_conditional)
    workflow.add_node(ASSIGN_TOOLS, invoke_tools)
    workflow.add_node(RESPONSE, produce_response) # adding the response 
    workflow.add_node(ACTIVATE_TASK_CONDITIONAL, activate_task)
    workflow.add_node(TIME_TASK_CONDITIONAL, time_duration)
    workflow.add_edge(TASK_CALL_CONDITIONAL, ASSIGN_TOOLS)
    workflow.add_conditional_edges(ASSIGN_TOOLS, activate_task_or_respond) # If no tools assigned, it will just return a default text
    workflow.add_conditional_edges(ACTIVATE_TASK_CONDITIONAL, time_task_or_respond)
    workflow.add_edge(ACTIVATE_TASK_CONDITIONAL, RESPONSE)
    # workflow.add_conditional_edges(MODEL_CALL, invoke_tools_or_respond) # If no tools assigned, it will just return a default text
    # workflow.add_edge(ASSIGN_TOOLS, RESPONSE)
    workflow.set_entry_point(TASK_CALL_CONDITIONAL) # starting point is the calling the model
    workflow.set_finish_point(RESPONSE) # end point is assigning and calling the tools or the END point which is the text response 

    graph = workflow.compile()
    return graph