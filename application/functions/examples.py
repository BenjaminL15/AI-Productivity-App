from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    MessagesPlaceholder,
)

examples_create_task = [
    {"input": "I need to plan a party for my sister", "output": '{"description": "Plan party for sister"}'},
    {"input": "My goal is to figure out what I should write in my email to my professor", "output": '{"description": "Create guest list for the party"}'},
    {"input": "Im trying to organize my notes for my exam", "output": '{"description": "Organizing notes for exam"}'},
    {"input": "I have to finish the presentation slides for the meeting", "output": '{"description": "Finish presentation slides for meeting"}'},
    {"input": "My project team needs to discuss our final report", "output": '{"description": "Discuss final report with project team"}'},
    {"input": "The plumber needs to be called about the kitchen sink", "output": '{"description": "Call plumber about kitchen sink"}'},
    {"input": "Grocery shopping for the week needs to be done", "output": '{"description": "Buy groceries for the week"}'},
    {"input": "Write a thank you note to express gratitude to a friend", "output": '{"description": "Write thank you note to friend"}'},
]

examples_invoke_model = [
    {"input": "I need to plan a party for my sister","output": '{"create_task": "yes"}'},
    {"input": "There needs to be a prize for the event", "output": '{"create_task": "yes"}'},
    {"input": "Thank you! I appreciate it!", "output": '{"create_task": "no"}'},
    {"input": "Sounds good! I will get right on it", "output": '{"create_task": "no"}'},
    {"input": "There needs to be a prize for the event", "output": '{"create_task": "yes"}'},
    {"input": "I need to buy decorations for the party", "output": '{"create_task": "yes"}'},
    {"input": "Can you help me find a DJ?", "output": '{"create_task": "yes"}'},
    {"input": "That's all for now, thanks!", "output": '{"create_task": "no"}'},
    {"input": "We need to order a cake", "output": '{"create_task": "yes"}'},
    {"input": "Don't worry about it, I've got it covered", "output": '{"create_task": "no"}'},
    {"input": "I need to send out invitations", "output": '{"create_task": "yes"}'},
    {"input": "The location is already booked", "output": '{"create_task": "no"}'},
    {"input": "Can you remind me to call the caterer?", "output": '{"create_task": "yes"}'},
    {"input": "Thanks for your help!", "output": '{"create_task": "no"}'},
    {"input": "I need to set up a photo booth", "output": '{"create_task": "yes"}'},
    {"input": "Hey, we need to discuss the project timeline", "output": '{"create_task": "no"}'},
    {"input": "Sure, what are the main tasks?", "output": '{"create_task": "no"}'},
    {"input": "First, we need to finalize the project scope", "output": '{"create_task": "yes"}'},
    {"input": "Okay, I'll draft the scope document", "output": '{"create_task": "yes"}'},
    {"input": "Great, we also need to assign team roles", "output": '{"create_task": "yes"}'},
    {"input": "I'll coordinate with HR on team assignments", "output": '{"create_task": "yes"}'},
    {"input": "We should also create a project schedule", "output": '{"create_task": "yes"}'},
    {"input": "I'll work on the project timeline", "output": '{"create_task": "yes"}'},
    {"input": "Thanks! Don't forget to set up progress meetings", "output": '{"create_task": "yes"}'},
    {"input": "Noted. I'll schedule weekly check-ins", "output": '{"create_task": "yes"}'},
    {"input": "Is there anything else we need to prepare?", "output": '{"create_task": "no"}'},
    {"input": "Yes, we need to allocate the budget", "output": '{"create_task": "yes"}'},
    {"input": "I'll review the budget proposal", "output": '{"create_task": "yes"}'},
    {"input": "Perfect, thank you!", "output": "{'create_task': 'no'}"},
    {"input": "No problem, happy to help!", "output": '{"create_task": "no"}'},
]

examples_time_task = [
    {"input": "I need to plan a party for my sister", "output": "20"},
    {"input": "My goal is to figure out what I should write in my email to my professor", "output": "10"},
    {"input": "I'm trying to organize my notes for my exam", "output": "15"},
    {"input": "Grocery shopping for the week needs to be done", "output": "59"},
    {"input": "The plumber needs to be called about the kitchen sink", "output": "30"},
]

examples_activate_task = [
    {
        "input": [
        ("user", "I need to plan a party for my mom"),
        ("assistant", "Planning a party for your mom can be a big task! Let's break it down together. \nTo get started, can you tell me what's the most important thing to you about this party? Is it the guest list, the theme, the food, or something else?"),
        ("user", "Food is the most important, so I need to set that up"),
        ("assistant", "Food is a crucial part of any party. Let's focus on that for now. \nWhat type of food are you thinking of serving? Is it going to be a full meal, appetizers and snacks, or just desserts?"),
        ("user", "It should just be snacks"),
        ("assistant", "Snacks are a great option for a party. Now let's narrow it down a bit more. \nAre you planning to make the snacks yourself, or would you like to order them from a catering service or store?"),
        ("user", "I need to order them from a catering service"),
        ("assistant", "Ordering from a catering service can save you a lot of time and effort. \nWhat's the next step you need to take to order from a catering service? Do you need to research and find a service, or do you already have one in mind?"),
        ("user", "I dont know what catering service to call")
        ],
        "task": "Research catering services",
        "output": """{
            "activate_task": "yes",
            "confidence": 0.9,
            "reasoning": "The task 'Research catering services' is specific, immediately actionable, can be completed in a short timeframe, requires no further planning, and is a focused action. The conversation shows a clear progression from a broad party planning task to this specific, necessary step."
        }"""
    },

    {
        "input": [
            ("user", "I need to study for an exam"),
            ("assistant", "Studying for an exam can feel overwhelming! \nLet's break it down together. What's the first thing that comes to mind when you think about studying for this exam? Is it a specific topic, chapter, or concept that you need to focus on?"),
            ("user", "It's a data structures and algorithms exam"),
            ("assistant", "Data structures and algorithms can be a challenging topic! \nLet's narrow it down further. Are there any specific data structures or algorithms that you're struggling with or feel less confidence about such as arrays, linked lists, stacks or sorting algorithms?"),
            ("user", "I need to review linked lists"),
            ("assistant", "Linked lists are a fundamental data structure! \nWhat's one specific aspect of linked lists that you'd like to review or feel uncertain about, such as inserting nodes, deleting nodes, or traversing the list?"),
            ("user", "I need to organize my notes for Linked lists")
        ],
        "task": "Organize notes for linked lists",
        "output": """{
            "activate_task": "yes",
            "confidence": 0.8,
            "reasoning": "The task 'Organize notes for linked lists' is specific, immediately actionable, and focused. It's a clear next step in the study process. However, the timeframe for completion might vary depending on the amount of notes, which slightly reduces the confidence score."
        }"""
    },
    {
        "input": [
            ("user", "I need to redecorate my living room"),
            ("assistant", "Redecorating a living room is a great project! \nLet's break it down step by step. What is the most important aspect for you? Is it the furniture, the color scheme, the lighting, or something else?"),
            ("user", "The color scheme is the most important"),
            ("assistant", "A good color scheme can set the tone for the whole room. \nDo you have any specific colors or themes in mind, or would you like some suggestions?"),
            ("user", "I need suggestions for colors that would go well with my existing furniture"),
            ("assistant", "Sure, let's figure that out. \nWhat is the dominant color or material of your existing furniture?"),
            ("user", "My furniture is mostly dark wood"),
            ("assistant", "Dark wood furniture can be complemented beautifully with a variety of colors. \nDo you prefer a warm, cozy feel with earthy tones, or a bright, airy atmosphere with lighter colors?"),
            ("user", "I prefer a warm, cozy feel"),
            ("assistant", "Great choice! \nThe next step would be to look at some specific color palettes. Would you like to search for some inspiration online, or do you have any sources in mind?"),
            ("user", "I need to search for inspiration online")
        ],
        "task": "Search for color scheme inspiration online",
        "output": """{
            "activate_task": "yes",
            "confidence": 0.95,
            "reasoning": "The task 'Search for color scheme inspiration online' is highly specific, immediately actionable, can be completed quickly, requires no further planning, and is a focused action. The conversation shows a clear progression from a broad redecorating task to this specific, necessary step for choosing a color scheme."
        }"""
    },
    {
        "input": [
            ("user", "I need to create a website for my small business"),
            ("assistant", "Creating a website is a fantastic way to promote your business! \nLet's start by identifying what's most important for your website. Is it the design, the content, the functionality, or something else?"),
            ("user", "The design is the most important"),
            ("assistant", "Design plays a crucial role in attracting and retaining visitors. \nDo you have any specific ideas or themes in mind for the design, or would you like some help with inspiration?"),
            ("user", "I need help with design inspiration"),
            ("assistant", "No problem! \nAre there any websites that you admire or would like to take inspiration from? If so, what do you like about them?"),
            ("user", "I like websites that are clean and minimalist"),
            ("assistant", "Clean and minimalist designs are very popular and effective. \nThe next step is to gather some examples of such designs. Do you want to search for design inspiration online, or do you have any sources you typically refer to?"),
            ("user", "I need to search for design inspiration online")
        ],
        "task": "Search for minimalist website design inspiration online",
        "output": """{
            "activate_task": "yes",
            "confidence": 0.95,
            "reasoning": "The task 'Search for minimalist website design inspiration online' is highly specific, immediately actionable, can be completed quickly, requires no further planning, and is a focused action. The conversation shows a clear progression from a broad website creation task to this specific, necessary step for gathering design inspiration."
        }"""
    },
    {
        "input": [
            ("user", "I need to file a loan for a house")
        ],
        "task": "file a loan for a house",
        "output": """{
            "activate_task": "no",
            "confidence": 0.9,
            "reasoning": "The task 'file a loan for a house' is too broad and complex to be an immediately actionable task. It involves multiple steps, requires gathering various documents, and cannot be completed in a short timeframe. The task needs to be broken down into smaller, more specific actions before it can be activated."
        }"""
    },
    {
        "input": [
            ("user", "I wan't to learn how to swim"),
            ("assistant", "Learning how to swim is a great goal! \nDo you already have any current swimming experience?"),
            ("user", "I have no swimming experience. The first stroke I want to learn is freestyle")
        ],
        "task": "learn freestyle stroke",
        "output": {
            "activate_task": "no",
            "confidence": 0.85,
            "reasoning": "The task 'learn freestyle stroke' is not immediately actionable for a beginner with no swimming experience. It's a complex skill that requires multiple steps, preparation, and likely professional instruction. The task needs to be broken down into more basic, preliminary steps such as finding a swimming class or instructor, learning water safety, or practicing basic water comfort exercises."
        }
    }
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{input}"),
        ("assistant", "{output}"),
    ]
)

example_activate_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Here is the conversation between the user and the assistant: {input}"),
        ("system", "task created: {task}\n should task be activated?"),
        ("assistant", "{output}"),
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

activate_shot_prompt = FewShotChatMessagePromptTemplate (
    example_prompt=example_activate_prompt,
    examples=examples_activate_task,
)