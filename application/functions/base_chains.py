from langchain_groq import ChatGroq
from firebase_functions.params import StringParam
from firebase_admin import credentials


# CRED = credentials.Certificate("./secret.json")
GROQ_API_KEY = StringParam("GROQ_API")

def create_llm():
    return ChatGroq(
        temperature=0,
        model="llama3-70b-8192",
        api_key=GROQ_API_KEY.value
    )
