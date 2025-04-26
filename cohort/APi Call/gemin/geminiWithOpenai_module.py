from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

result = client.chat.completions.create(
    model = "gemini-2.0-flash",
    messages = [
    {"role": "system", "content": "You are helpfull assitent"},
    {"role":"user","content":"What is 2+2"}
        ]
)

print(result.choices[0].message.content)
print(result.usage.total_tokens)
