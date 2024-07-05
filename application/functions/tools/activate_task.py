from typing import Optional
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from base_chains import BaseChain

class RecentMessages(BaseModel):
    input: str = Field(..., description="recent messages between the user and ai assistant")
class ActionableTask(BaseModel):
    task: str = Field(..., description="the most immediate task the user has agreed to complete")
    duration: int = Field(..., description="the approximate amount of minutes the task should take to complete")

@tool("create_actionable_task", args_schema=RecentMessages, return_direct=True)
def create_actionable_task(chat_history: str):
    """Create a task that the user will try to complete within a couple of minutes."""
        
    actionable_task_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert in identifying the most immediate task that the user has agreed to complete.
                You will be provided with the recent messages between the user and the AI assistant who are trying 
                to break down a task into its most essential forms. Respond by summarizing the immediately actionable
                task in a very concise and clear way that is no longer than 1 sentance. Then consider how many 
                minutes the task should take. If the duration has already been suggested in conversation then select 
                that time for the duration.\n
                In case there is no clear immediate task that has been agreed upon then do not call your function.\n
                The response should be in the form of a JSON object with the keys 'task' and 'duration'""",
            ),
            (
                "user",
                "Here is the recent conversation messages: {chat_history}"
            ),
        ]
    )
    model = BaseChain.create_llm()
    stuctered_model = model.with_structured_output(ActionableTask, method="json_mode")
    chain = actionable_task_prompt | stuctered_model
    result = chain.invoke({"chat_history": chat_history})

    if not isinstance(result, AIMessage):
        raise ValueError("Invalid result from model. Expected AIMessage.")
    if result.tool_calls:
        return result.tool_calls[0]
    else:
        return None