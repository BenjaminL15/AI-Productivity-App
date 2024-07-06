
from typing import List, Optional, TypedDict
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langgraph.graph import END, StateGraph  # not sure about the from langgraph import stuff 
from langgraph.graph.graph import CompiledGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables  import RunnableConfig
from base_chains import BaseChain
from tools.activate_task import create_actionable_task

class GenerativeUIState(TypedDict, total=False):
    input: Optional[List[(str, str)]]
    result: Optional[str]
    # parsed tool calls
    tool_calls: Optional[List[dict]]
    # result of the tool calls
    tool_result: Optional[dict]

def invoke_model(state: GenerativeUIState, config: RunnableConfig) -> GenerativeUIState:
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

    model = BaseChain.create_llm()
    model_with_tools = model.bind_tools(create_actionable_task)
    chain = INITIAL_PROMPT | model_with_tools
    result = chain.invoke(config)

    if isinstance(result.tool_calls, list) and len(result.tool_calls) > 0:
        parsed_tools = tools_parser.invoke(result, config)
        return {"tool_calls": parsed_tools}
    
def invoke_tools_or_respond(state: GenerativeUIState) -> str:
    if "tool_calls" in state and isinstance(state["tool_calls"], list):
        return "invoke_tools" 
    else:
        return "produce_response"
    
def invoke_tools(state: GenerativeUIState) -> GenerativeUIState:
    tools_map = {
        "activate-task": create_actionable_task
    }

    if state["tool_calls"] is not None:
        tool = state["tool_calls"][0]
        selected_tool = tools_map[tool["type"]]
        return {"tool_result": selected_tool.invoke(tool["args"])}
    else:
        raise ValueError("No tool calls found in state.")
    
def produce_response(state: GenerativeUIState, config: RunnableConfig) -> str:
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
    model = BaseChain.create_llm()
    chain = RESPONSE_PROMPT | model | StrOutputParser()
    result = chain.invoke(config)

    return {"input" : [("system",result)] }

def create_graph() -> CompiledGraph:

    workflow = StateGraph(GenerativeUIState)

    workflow.add_Node("Calling the model", invoke_model) # This part calls the AI and it will decide what to respond with
    workflow.add_Node("Assigning the tools", invoke_tools) # This basically assigns and calls the tools that the AI is assigned to or return plain text
    workflow.add_Node("Producing the response", produce_response) # adding the response 
    workflow.add_conditional_edges("Calling model", invoke_tools_or_respond) # If no tools assigned, it will just return a default text
    workflow.add_edge("Assigning the tools", "Producing the response")
    workflow.set_entry_point("Calling the model") # starting point is the calling the model
    workflow.set_finish_point("Producing the response") # end point is assigning and calling the tools or the END point which is the text response 

    graph = workflow.compile()
    return graph