from typing import List, Optional, TypedDict
from langgraph.graph import END, StateGraph  # not sure about the from langgraph import stuff 
from langgraph.graph.graph import CompiledGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables  import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from base_chains import ChatGroqSingleton
from create_task import create_task
from examples import model_shot_prompt, activate_shot_prompt, time_shot_prompt


ASSIGN_TOOLS = "Assigning the tools"
RESPONSE = "Producing the response"
TASK_CALL_CONDITIONAL = "Decide if we want to create a task"
ACTIVATE_TASK_CONDITIONAL = "Decide if we want to activate a task"
TIME_TASK_CONDITIONAL = "Determine if the task is activated"
CREATE_ACTIONABLE_TASK = "Create an actionable task"

class GenerativeUIState(TypedDict, total=False):
    input: List[tuple]
    tasks: List[dict]
    result: Optional[str]
    # parsed tool calls
    tool_calls: Optional[set]
    # result of the tool calls
    tool_results: Optional[dict]

class Task(TypedDict):
    description: str
    duration: Optional[int]
    active: Optional[bool]

class DecideTaskCreation(BaseModel):
    create_task: str = Field(description= "decide whether or not to create a task")

def create_task_conditional(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
    print("CREATE TASK CONDITIONAL")
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
    tasks = [task["description"] for task in state["tasks"]]
    result = chain.invoke({"input": state["input"], "tasks": tasks}, config)
    print(f"INVOKE TOOL result: {result}, type is {type(result)}")
    if not isinstance(result, dict):
        raise ValueError("Invalid result from model. Expected AIMessage.")
    
    if result["create_task"] == "yes":
        return {"tool_calls": {"create_task"}}

def invoke_tools(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
    print(f"INVOKE TOOLS: {state['tool_calls']}")

    state["tool_results"] = {}


    task = create_task()
    tools_map = {
        "create_task": task
    }

    if state["tool_calls"] is None:
        return
    
    print(f"pre tool call itteration")
    for tool_call in state["tool_calls"]:
        print(f"inside the loop: {tool_call}")
        print(f"inside the loop state['input'] type is: {type(state['input'])}")
        selected_tool = tools_map[tool_call]
        result = selected_tool.invoke({"input":state["input"]})
        print("MADE IT THROUGH THE TOOL CALL")
        print(f"result of tool call: {result}")
        match tool_call:
            case "create_task":
                print("converting create_task graph into real task")
                new_task = Task(description= result["description"], duration= result["duration"], active= result["active"])
                return {"tool_results": {tool_call: new_task}, "tasks": state["tasks"] + [new_task]}
                # state["tool_results"][tool_call] = new_task
                # state["tasks"] = state["tasks"] + [new_task]

def produce_response(state: GenerativeUIState, config: RunnableConfig) -> str:
    print("we are at the produce response")

    if state["tool_calls"] and "activate_task" in state["tool_calls"]:
        if state['tool_results']["create_task"]["active"] == True:
            state["input"].append(("system", f"prompt the user to commit to the task: {state['tasks'][-1]}"))

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
    workflow.add_node(RESPONSE, produce_response)
    workflow.add_edge(TASK_CALL_CONDITIONAL, ASSIGN_TOOLS)
    workflow.add_edge(ASSIGN_TOOLS, RESPONSE)

    workflow.set_entry_point(TASK_CALL_CONDITIONAL) # starting point is the calling the model
    workflow.set_finish_point(RESPONSE) # end point is assigning and calling the tools or the END point which is the text response 

    graph = workflow.compile()
    return graph