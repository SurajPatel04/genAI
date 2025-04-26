from openai import OpenAI
from dotenv import load_dotenv
from retrieval import retrieve
import os


load_dotenv()

def ai(message):
    response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=message,
    )
    return response.choices[0].message.content


client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.

    Answer should be in detail
    You recive a question and you give answer 
"""
query = input("> ")
message=[{"role":"system","content":system_prompt},{"role":"user","content":query}]
llm_answer = ai(message) 

print("\nLLM Answer: ")
print(llm_answer)

relevant_chunk = retrieve(llm_answer)


