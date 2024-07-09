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

examples_invoke_model = [
    {"input": "I need to plan a party for my sister", "output": {"create_task": 'yes'}},
    {"input": "There needs to be a prize for the event", "output": {"create_task": 'yes'}},
    {"input": "Thank you! I appreciate it!", "output": {"create_task": 'no'}},
    {"input": "Sounds good! I will get right on it", "output": {"create_task": 'no'}},
    {"input": "There needs to be a prize for the event", "output": {"create_task": 'yes'}},
    {"input": "I need to buy decorations for the party", "output": {"create_task": "yes"}},
    {"input": "Can you help me find a DJ?", "output": {"create_task": "yes"}},
    {"input": "That's all for now, thanks!", "output": {"create_task": "no"}},
    {"input": "We need to order a cake", "output": {"create_task": "yes"}},
    {"input": "Don't worry about it, I've got it covered", "output": {"create_task": "no"}},
    {"input": "I need to send out invitations", "output": {"create_task": "yes"}},
    {"input": "The location is already booked", "output": {"create_task": "no"}},
    {"input": "Can you remind me to call the caterer?", "output": {"create_task": "yes"}},
    {"input": "Thanks for your help!", "output": {"create_task": "no"}},
    {"input": "I need to set up a photo booth", "output": {"create_task": "yes"}},
    {"input": "Hey, we need to discuss the project timeline", "output": {"create_task": "no"}},
    {"input": "Sure, what are the main tasks?", "output": {"create_task": "no"}},
    {"input": "First, we need to finalize the project scope", "output": {"create_task": "yes"}},
    {"input": "Okay, I'll draft the scope document", "output": {"create_task": "yes"}},
    {"input": "Great, we also need to assign team roles", "output": {"create_task": "yes"}},
    {"input": "I'll coordinate with HR on team assignments", "output": {"create_task": "yes"}},
    {"input": "We should also create a project schedule", "output": {"create_task": "yes"}},
    {"input": "I'll work on the project timeline", "output": {"create_task": "yes"}},
    {"input": "Thanks! Don't forget to set up progress meetings", "output": {"create_task": "yes"}},
    {"input": "Noted. I'll schedule weekly check-ins", "output": {"create_task": "yes"}},
    {"input": "Is there anything else we need to prepare?", "output": {"create_task": "no"}},
    {"input": "Yes, we need to allocate the budget", "output": {"create_task": "yes"}},
    {"input": "I'll review the budget proposal", "output": {"create_task": "yes"}},
    {"input": "Perfect, thank you!", "output": {"create_task": "no"}},
    {"input": "No problem, happy to help!", "output": {"create_task": "no"}},
]

examples_time_task = [
    {
        "input": "I need to plan a party for my sister",
        "output": {
            "task": "Plan party for sister",
            "time": "45 minutes",
            "task_history": {
                "Decide on the theme": "5 minutes",
                "Create a guest list": "10 minutes",
                "Send out invitations": "5 minutes",
                "Plan the menu": "10 minutes",
                "Buy decorations and supplies": "10 minutes",
                "Set up the party area": "15 minutes"
            }
        }
    },
    {
        "input": "My goal is to figure out what I should write in my email to my professor",
        "output": {
            "task": "Figure out email content for professor",
            "time": "30 minutes",
            "task_history": {
                "List key points to include": "10 minutes",
                "Draft the email": "10 minutes",
                "Review and edit the email": "10 minutes"
            }
        }
    },
    {
        "input": "I'm trying to organize my notes for my exam",
        "output": {
            "task": "Organize notes for exam",
            "time": "1 hour",
            "task_history": {
                "Gather all notes": "20 minutes",
                "Sort notes by topic": "20 minutes",
                "Highlight key information": "10 minutes",
                "Create summary sheets": "10 minutes"
            }
        }
    },
    {
        "input": "Grocery shopping for the week needs to be done",
        "output": {
            "task": "Buy groceries for the week",
            "time": "30 minutes",
            "task_history": {
                "Make a shopping list": "10 minutes",
                "Drive to grocery store": "5 minutes",
                "Shop for items": "10 minutes",
                "Return home and unpack": "5 minutes"
            }
        }
    },
    {
        "input": "The plumber needs to be called about the kitchen sink",
        "output": {
            "time": "30 minutes",
            "task_history": {
                "Call plumber about kitchen sink",
                "Find plumber's contact info",
                "Call and explain the issue",
                "Schedule appointment"
            }
        }
    },
]



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

model_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples_invoke_model,
)

time_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples_time_task,
)