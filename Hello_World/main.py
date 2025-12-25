from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI(
    api_key="AIzaSyCAGpePHnbvDg5NmS_Ou6n8dtxTJ6sAp_4",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You expert in math and only and only answer math related questions .If  the query is not related to math do not answer say sorry i can anwer only math related questions"},
        {
            "role": "user",
            "content": "Help me solve 8 multiplied by 4"
        }
    ]
)

print(response.choices[0].message.content)