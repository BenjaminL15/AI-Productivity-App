from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

examples_create_task = [
    {"input": "I need to plan a party for my sister", "output": "Plan party for sister"},
    {"input": "My goal is to figure out what I should write in my email to my professor", "output" : "Create guest list for the party"},
    {"input": "Im trying to organize my notes for my exam", "output" : "Organizing notes for exam"},
    {"input": "I have to finish the presentation slides for the meeting", "output": "Finish presentation slides for meeting"},
    {"input": "My project team needs to discuss our final report", "output": "Discuss final report with project team"},
    {"input": "The plumber needs to be called about the kitchen sink", "output": "Call plumber about kitchen sink"},
    {"input": "Grocery shopping for the week needs to be done", "output": "Buy groceries for the week"},
    {"input": "Write a thank you note to express gratitude to a friend", "output": "Write thank you note to friend"},
]

# examples_invoke_model = [
#     {"input": "I need to plan a party for my sister", "output": }
# ]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("assistant", "{output}"),
        ("user", "{input}"),
    ]
)

create_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples_create_task,
)