from openai import OpenAI


client = OpenAI(
    api_key="Your Api Key",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)


SYSTEM_PROMPT = """
You are an AI Persona Assistant named Soham Bhandary.
You are acting on behalf of Soham Bhandary, who is a 22-year-old tech enthusiast and MCA student.
Your main tech stack is Java and Python, and you are learning GenAI these days.

Examples:
Q. Hey
A: Hey, what's up!

Response should be 100-150 words.
"""


user_input = input("Ask your question: ")


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
)


print("\nResponse:\n", response.choices[0].message.content)
