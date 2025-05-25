import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import json


os.environ["GROQ_API_KEY"] = "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"

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=1,
    request_timeout=10
)



def generate_question(topic, mastery):
    if mastery < 0.3:
        level = "easy"
    elif mastery < 0.7:
        level = "intermediate"
    else:
        level = "hard"

    prompt = PromptTemplate(
        template="""
        Generate a {level} difficulty multiple-choice question on the topic: {topic}.
        The question should have exactly 4 options, with one correct answer.
        Return your response in JSON format like this:

        {{
            "question": "<question text>",
            "options": ["option1", "option2", "option3", "option4"],
            "correct_answer": "<correct option>"
        }}
        """,
        input_variables=["level", "topic"]
    )

    formatted_prompt = prompt.format(level=level, topic=topic)
    response = llm.invoke(formatted_prompt)

    print(level)
    return response.content
    # except json.JSONDecodeError as e:
    #     print("Failed to parse question JSON:", e)
    #     # fallback: return just raw text or empty dict
    #     return {"question": response.content, "options": [], "correct_answer": ""}



def evaluate_answer(question, answer, topic=None):
    try:
        print(f"Starting evaluation for topic: {topic}")  # Debug print

        prompt = f"""
        Question: {question}
        Student Answer: {answer}
        Topic: {topic}

        Evaluate this answer and give:
        1. A score between 0 and 1
        2. Brief feedback
        3. Correction if needed

        Return only JSON like this: {{"score": 0.8, "feedback": "Good job!", "correction": "None needed"}}
        """

        print("Sending prompt to LLM...")  # Debug print
        response = llm.invoke(prompt)
        print(f"LLM Response received: {response.content}")  # Debug print

        result = json.loads(response.content.strip())
        return result

    except Exception as e:
        print(f"Error in evaluate_answer: {str(e)}")  # Debug print
        return {
            "score": 0.0,
            "feedback": f"Error during evaluation: {str(e)}",
            "correction": "Please try again"
        }

# result = evaluate_answer(
#     question="Given a 2x2 matrix A, where A = [[4, 3], [3, 2]], find the determinant of the matrix and also find the eigenvalues of the matrix",
#     answer="45",
#     topic="algebra"
# )
#
# print(result)

# Test case
# if __name__ == "__main__":
#     print("Testing evaluation...")
#     test_result = evaluate_answer(
#         question="Given a 2x2 matrix A, where A = [[4, 3], [3, 2]], find the determinant of the matrix and also find the eigenvalues of the matrix",
#         answer="45",
#         topic="algebra"
#     )
#     print("Result:", test_result)

print(generate_question('algebra',0.9))