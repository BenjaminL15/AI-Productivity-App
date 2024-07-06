from typing import Optional
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from firebase_functions.params import StringParam
from base_chains import create_llm

class RecentMessages(BaseModel):
    input: str = Field(..., description="recent messages between the user and ai assistant")
class ActionableTask(BaseModel):
    task: str = Field(..., description="concise summary of the task the user wants to complete")

@tool("create_actionable_task", args_schema=RecentMessages, return_direct=True)
def create_actionable_task(chat_history: str):
    """Create a task that the user will try to complete within a couple of minutes."""
        
    actionable_task_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert in identifying the task.
                You will be provided with the recent messages between the user and the AI assistant. Respond by summarizing the 
                task in a very concise and clear way that excludes specific details.\n
                In case there is no clear immediate task that has been agreed upon then set task to none.\n
                The response should be in the form of a JSON object with the keys 'task'""",
            ),
            (
                "user",
                "Here is the recent conversation messages: {input}"
            ),
        ]
    )

    model = create_llm()
    stuctered_model = model.with_structured_output(ActionableTask, method="json_mode")
    chain = actionable_task_template | stuctered_model
    result = chain.invoke({"input" : chat_history})

    # if not isinstance(result, AIMessage):
    #     raise ValueError("Invalid result from model. Expected AIMessage.")
    if result:
        return result
    else:
        return None
    

# print(create_actionable_task("Hey, I have a task"))
