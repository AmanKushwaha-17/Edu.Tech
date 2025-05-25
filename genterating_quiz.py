import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import json


os.environ["GROQ_API_KEY"] = ""

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=1,
    request_timeout=10
)

def quiz(topic,mastery=0):
    if mastery < 0.3:
        level = "easy"
    elif mastery < 0.7:
        level = "intermediate"
    else:
        level = "hard"
    prompt = PromptTemplate(
        template="""
            Generate exactly 5 {level} difficulty multiple-choice questions on the topic: {topic}.
            Each question should have 4 options, with exactly one correct answer.
            Return your response as a JSON list like this:

            [
                {{
                    "question": "<question text>",
                    "options": ["option1", "option2", "option3", "option4"],
                    "correct_answer": "<correct option>"
                }},
                ...
                (5 questions total)
            ]
            """,
        input_variables=["level", "topic"]
    )
    print(level)
    formatted_prompt = prompt.format(level=level, topic=topic)
    response = llm.invoke(formatted_prompt)
    return response.content.strip()

print(quiz("algebra", 0.8))

