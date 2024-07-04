# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

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

# firebase_admin.initialize_app(cred)
client = Groq(api_key=GROQ_API_KEY.value)

app = initialize_app()



@https_fn.on_call()
def test(req: https_fn.CallableRequest) -> https_fn.Response:
    """Saves a message to the Firebase Realtime Database but sanitizes the text
    by removing swear words."""
    data = req.data
    chat_history: List[Dict] = data['messages']
    input = data['inputText']
    messages_for_prompt = format_chat_history(chat_history, input)

    chat_completiton = client.chat.completions.create(
        messages= messages_for_prompt,
        model= "llama3-70b-8192"
    )
    return {"response": chat_completiton.choices[0].message.content}