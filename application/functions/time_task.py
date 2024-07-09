from typing import Optional, List
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from firebase_functions.params import StringParam
from base_chains import ChatGroqSingleton
from examples import time_shot_prompt

class RecentMessages(BaseModel):
    input: List[tuple] = Field(..., description="provide recent messages between the user and ai assistant")
class Task(BaseModel):
    time: int = Field(..., description="The exact time needed to complete the task")

@tool("time_task", args_schema=RecentMessages, return_direct=True)
def time_task(input: str):
    """Determine the duration of a task that is within 60 minutes"""
        
    task_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert at determining the duration of the tasks given.
                You will be provided with the recent messages between the user and the AI assistant along with a list of tasks. Respond by giving the user
                the estimated time taken to complete task after it has been broken down significantly.\n
                In case there is already a time duration already given for the task, then do not assign a time.\n
                The response should be in the form of a JSON object with the keys 'time'""",
            ),
            time_shot_prompt,
            MessagesPlaceholder("input")
        ]
    )

    model = ChatGroqSingleton().get_llm()
    stuctered_model = model.with_structured_output(Task, method="json_mode")
    chain = task_template | stuctered_model
    result = chain.invoke({"input" : input})

    # if not isinstance(result, AIMessage):
    #     raise ValueError("Invalid result from model. Expected AIMessage.")
    if result:
        return result
    else:
        return None
    

# print(create_task("Hey, I have a task"))