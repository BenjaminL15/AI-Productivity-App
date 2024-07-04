from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from base_chains import BaseChain
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict
SUMMARY_SYSTEM_PROMPT = """You are an expert in sumarizing conversations between an AI assistant
                           and a user who is trying to break down a task. Summarize the conversation 
                           while capturing important topics, and details needed for future planning.
                           Be concise and clear in your summary."""

def format_chat_history(raw_chat: List[Dict], input: str) -> List[(str, str)]:
            """Formats the chat history to be compatible with the OpenAI chat completion API."""
            formatted_chat_history = []
            for message in reversed(raw_chat):
                text = message.get('text', '')
                respondent = message.get('user', '')
                formatted_chat_history.append((respondent, text))
            formatted_chat_history.append(("user", input))
            return formatted_chat_history

class SetupChain(BaseChain):
    def __init__(self):
        self.model = super().create_llm()
        
    def create_chat_summary_chain(self, messages: List[(str, str)]) -> str:
        """Creates a summary of the chat history for the user."""
        summary_prompt = ChatPromptTemplate.from_messages(messages + [("system", SUMMARY_SYSTEM_PROMPT)] )

        summary_chain = summary_prompt | self.model | StrOutputParser()

        return summary_chain
    
    def router_chain(self):
        synopsis_prompt = ChatPromptTemplate.from_messages([
             

        ]
             """Here is the summary of the current conversation: \n\n {summary} \n\n
                For context of the conversation's most recent details the last messages have been provided: \n\n
                {messages}

             """
        )