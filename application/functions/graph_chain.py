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
from examples import model_shot_prompt



ASSIGN_TOOLS = "Assigning the tools"
RESPONSE = "Producing the response"
MODEL_CALL = "Calling the model"

class GenerativeUIState(TypedDict, total=False):
    input: List[tuple]
    tasks: List[str]
    result: Optional[str]
    # parsed tool calls
    tool_calls: Optional[List[str]]
    # result of the tool calls
    tool_results: Optional[dict]

class DecideTaskCreation(BaseModel):
    create_task: str = Field(description= "decide whether or not to create a task")


def produce_response(state: GenerativeUIState, config: RunnableConfig) -> str:
    print("we are at the produce response")

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

def invoke_model(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
    print("We are at invoke_model")
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
        return {"tool_calls": ["create_task"]}
    print(f"no tool call made: {result}")

def invoke_tools(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
    print(f"post state tool calls: {state['tool_calls']}")

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
    print(tool_results)
    return {"tool_results": tool_results, "tasks": [tool_results[0].description]}




    # print("We are at invoke_tools")
    # create_test = create_task(str(state["input"]))
    # print(f"Create_task results : {create_test}")
    # return {"tool_result": [create_test]}

    # tools_map = {
    #     "activate-task": create_actionable_task
    # }

    # if state["tool_calls"] is not None:
    #     # tool = state["tool_calls"][0]
    #     # selected_tool = tools_map[tool["type"]]
    #     print("We reached the invoke tools end of if statement")
    # else:
    #     raise ValueError("No tool calls found in state.")

def create_graph() -> CompiledGraph:
    print("We are in create graph")

    workflow = StateGraph(GenerativeUIState)

    # workflow.add_node(MODEL_CALL, invoke_model) # This part calls the AI and it will decide what to respond with
    # workflow.add_node(ASSIGN_TOOLS, invoke_tools) # This basically assigns and calls the tools that the AI is assigned to or return plain text
    workflow.add_node(MODEL_CALL, invoke_model)
    workflow.add_node(ASSIGN_TOOLS, invoke_tools)
    workflow.add_node(RESPONSE, produce_response) # adding the response 
    workflow.add_edge(MODEL_CALL, ASSIGN_TOOLS)
    workflow.add_edge(ASSIGN_TOOLS, RESPONSE)
    # workflow.add_conditional_edges(MODEL_CALL, invoke_tools_or_respond) # If no tools assigned, it will just return a default text
    # workflow.add_edge(ASSIGN_TOOLS, RESPONSE)
    workflow.set_entry_point(MODEL_CALL) # starting point is the calling the model
    workflow.set_finish_point(RESPONSE) # end point is assigning and calling the tools or the END point which is the text response 

    graph = workflow.compile()
    return graph