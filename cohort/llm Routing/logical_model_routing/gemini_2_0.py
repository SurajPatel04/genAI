from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def gemini2_0(query):
    print("gemini2_0")
    client = OpenAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    message = [{"role":"system","content":"You are helpful ai assitant in the answer you should mention the model"},{"role":"user","content":query}]

    response = client.chat.completions.create(
                model="gemini-2.0-flash",
                response_format={"type":"json_object"},
                messages = message
        )
    
    return response.choices[0].message.content