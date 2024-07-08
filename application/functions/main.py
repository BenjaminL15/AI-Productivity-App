# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from groq import Groq
from typing import List, Dict
import os
from firebase_functions import https_fn, options
from firebase_functions.params import StringParam
from firebase_admin import db, initialize_app
import firebase_admin
from firebase_admin import credentials
from graph_chain import create_graph

CRED = credentials.Certificate("./secret.json")
# GROQ_API_KEY = StringParam("GROQ_API")
# firebase_admin.initialize_app(cred)
# client = Groq(api_key=GROQ_API_KEY.value)

app = initialize_app()

def format_chat_history(raw_chat: List[Dict], input: str) -> List[tuple]:
            """Formats the chat history to be compatible with the OpenAI chat completion API."""
            print("We are in format chat history")
            formatted_chat_history = []
            for message in reversed(raw_chat):
                text = message.get('text', '')
                respondent = message.get('user', '')
                formatted_chat_history.append((respondent, text))
            formatted_chat_history.append(("user", input))
            return formatted_chat_history

@https_fn.on_call()
def test(req: https_fn.CallableRequest) -> https_fn.Response:
    """Saves a message to the Firebase Realtime Database but sanitizes the text
    by removing swear words."""
    print("We are in test")
    data = req.data
    chat_history: List[Dict] = data['messages']
    task_history: List[str] = data['tasks']
    input = data['inputText']
    graph = create_graph()
    messages_for_prompt = format_chat_history(chat_history, input)
    print("We reached the end of this")
    ret = graph.invoke({"input" : messages_for_prompt, "tasks": task_history})
    print("We reached the invoke")
    
    print(ret)
    return {"response": ret["input"][-1][1], "tasks": ret["tasks"]}