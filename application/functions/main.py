# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`
from groq import Groq
import os
from firebase_functions import https_fn, options
from firebase_functions.params import StringParam
from firebase_admin import db, initialize_app
import firebase_admin
from firebase_admin import credentials

CRED = credentials.Certificate("./secret.json")
GROQ_API_KEY = StringParam("GROQ_API")
# firebase_admin.initialize_app(cred)
client = Groq(api_key=GROQ_API_KEY)

app = initialize_app()

@https_fn.on_call()
def test(req: https_fn.CallableRequest) -> https_fn.Response:
    """Saves a message to the Firebase Realtime Database but sanitizes the text
    by removing swear words."""
    text = req.data["text"]

    chat_completiton = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-70b-8192"
    )
    return {"response": chat_completiton.choices[0].message.content}