# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from graph_chain import create_graph
from typing import List, Dict

from firebase_functions import https_fn, options
from firebase_functions.params import StringParam
from firebase_admin import db, initialize_app
import firebase_admin
from firebase_admin import credentials


CRED = credentials.Certificate("./secret.json")
GROQ_API_KEY = StringParam("GROQ_API")
SYSTEM_PROMPT = "You are a helpful assistant that guides users in breaking down tasks.\
                 You make users feel heard while prompting them to think about their\
                 task and how it can be reduced or if they have already made progress\
                 towards said task. Keep reducing tasks until they can be completed\
                 within a couple of minutes. Make the user feel as little overwhelmed\
                 as possible. Ask one thing at a time to help pin point a first task\
                 that can be completed. Be concise."

app = initialize_app()

def format_chat_history(raw_chat: List[Dict], input: str) -> List[(str, str)]:
            """Formats the chat history to be compatible with the OpenAI chat completion API."""
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
    data = req.data
    chat_history: List[Dict] = data['messages']
    input = data['inputText']
    graph = create_graph()
    messages_for_prompt = format_chat_history(chat_history, input)
    ret = graph.invoke(input=messages_for_prompt)
    
    print(ret)
    return {"response": ret["input"][-1][1]}