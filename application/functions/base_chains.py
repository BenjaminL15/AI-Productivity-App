from langchain_groq import ChatGroq
from firebase_functions.params import StringParam
from firebase_admin import credentials

# CRED = credentials.Certificate("./secret.json")
GROQ_API_KEY = StringParam("GROQ_API")

class ChatGroqSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatGroqSingleton, cls).__new__(cls)
            cls._instance.llm = ChatGroq(
                temperature=0,
                model="llama3-70b-8192",
                api_key=GROQ_API_KEY.value
            )
        return cls._instance

    def get_llm(self):
        return self.llm