from typing import List, Optional, TypedDict
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langgraph.graph import END, StateGraph  # not sure about the from langgraph import stuff 
from langgraph.graph.graph import CompiledGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables  import RunnableConfig
from base_chains import create_llm
from activate_task import create_actionable_task

ASSIGN_TOOLS = "Assigning the tools"
RESPONSE = "Producing the response"
MODEL_CALL = "Calling the model"


class GenerativeUIState(TypedDict, total=False):
    input: List[tuple]
    result: Optional[str]
    # parsed tool calls
    tool_calls: Optional[List[dict]]
    # result of the tool calls
    tool_result: Optional[dict]

def invoke_model(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
    print("We reached the invoke model")
    tools_parser = JsonOutputToolsParser()
    INITIAL_PROMPT = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that will read the chat history with the user and deteremine whether.\
                or not the messages are relevant enough to invoke a tool or respond with relevant text."
            )
        ] + state["input"]
    )

    model = create_llm()
    model_with_tools = model.bind_tools([create_actionable_task])
    chain = INITIAL_PROMPT | model_with_tools
    result = chain.invoke(config)
    print("We reached the end of invoke model")

    if isinstance(result.tool_calls, list) and len(result.tool_calls) > 0:
        parsed_tools = tools_parser.invoke(result, config)
        return {"tool_calls": parsed_tools}
    
def invoke_tools_or_respond(state: GenerativeUIState) -> str:
    print("We reached the invoke tools or respond")
    if "tool_calls" in state and isinstance(state["tool_calls"], list):
        print("We reached the end of tools or respond")
        return ASSIGN_TOOLS 
    else:
        print("We reached the end of tools or respond else statement")
        return RESPONSE
    
def invoke_tools(state: GenerativeUIState) -> GenerativeUIState:
    print("We reached the invoke tools")
    tools_map = {
        "activate-task": create_actionable_task
    }

    if state["tool_calls"] is not None:
        tool = state["tool_calls"][0]
        selected_tool = tools_map[tool["type"]]
        print("We reached the invoke tools end of if statement")
        return {"tool_result": selected_tool.invoke(tool["args"])}
    else:
        raise ValueError("No tool calls found in state.")
    
def produce_response(state: GenerativeUIState, config: RunnableConfig) -> str:
    print("we are at the produce response")
    if "tool_calls" in state and isinstance(state["tool_calls"], list):
        tool_message = ""
        for tools in state["tool_result"]: 
            tool_message += str(tools)
        state["input"].append("assistant", tool_message)

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
    model = create_llm()
    chain = RESPONSE_PROMPT | model | StrOutputParser()
    result = chain.invoke(config)
    print("we are at the end of produce response")
    return {"input" : [("system", result)] }

def create_graph() -> CompiledGraph:
    print("We are in create graph")

    workflow = StateGraph(GenerativeUIState)

    workflow.add_node(MODEL_CALL, invoke_model) # This part calls the AI and it will decide what to respond with
    workflow.add_node(ASSIGN_TOOLS, invoke_tools) # This basically assigns and calls the tools that the AI is assigned to or return plain text
    workflow.add_node(RESPONSE, produce_response) # adding the response 
    workflow.add_conditional_edges(MODEL_CALL, invoke_tools_or_respond) # If no tools assigned, it will just return a default text
    workflow.add_edge(ASSIGN_TOOLS, RESPONSE)
    workflow.set_entry_point(MODEL_CALL) # starting point is the calling the model
    workflow.set_finish_point(RESPONSE) # end point is assigning and calling the tools or the END point which is the text response 

    graph = workflow.compile()
    return graph