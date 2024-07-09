from typing import Optional, List
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from firebase_functions.params import StringParam
from base_chains import ChatGroqSingleton
from examples import create_shot_prompt

class RecentMessages(BaseModel):
    input: List[tuple] = Field(..., description="provide recent messages between the user and ai assistant")
class Task(BaseModel):
    description: str = Field(..., description="concise but specific summary of the task the user wants to complete")

@tool("create_task", args_schema=RecentMessages, return_direct=True)
def create_task(input: str):
    """Create a task that the user will try to complete within a couple of minutes."""
        
    task_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert in identifying the task.
                You will be provided with the recent messages between the user and the AI assistant. Respond by summarizing the 
                task in a very concise and clear way that excludes specific details.\n
                The users most recent response is the most important while all other messages from the user and the ai should just be used for context.
                In case there is no clear immediate task that has been agreed upon then set task to none.\n
                The response should be in the form of a JSON object with the keys 'description'""",
            ),
            create_shot_prompt,
            MessagesPlaceholder("input")
        ]
    )

    model = ChatGroqSingleton().get_llm()
    stuctered_model = model.with_structured_output(Task)
    chain = task_template | stuctered_model
    result = chain.invoke({"input" : input})

    # if not isinstance(result, AIMessage):
    #     raise ValueError("Invalid result from model. Expected AIMessage.")
    if result:
        return result
    else:
        return None
    

# print(create_task("Hey, I have a task"))