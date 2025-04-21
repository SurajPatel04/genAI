from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

def answer_AI(query, assistant):
    system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.

    Note:
    Answer should be in detail
    You recive a question and you give answer based on the assistant content and 
    also Mention the page number from where did you pick all the information and
    If you add something from you then tell where did you added something
    """
    message =[{"role":"system","content":system_prompt},{"role":"user","content":query},{"role":"assistant","content":assistant}]
    response=client.chat.completions.create(
        model="gemini-1.0-flash",
        messages=message,
        response_format={"type":"json_object"}

    )

    return response.choices[0].message.content
