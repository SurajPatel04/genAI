from openai import OpenAI
from dotenv import load_dotenv
from retrieval import retrieve
from answer_ai import answer_AI
import os
import json

load_dotenv()

def ai(message):
    response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=message,
    response_format={"type":"json_object"}
    )
    return json.loads(response.choices[0].message.content)


client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
system_prompt = f"""
 You are an helpfull AI Assistant who is specialized in resolving user query.
 You break the user query into three or five different query.

Example: "What is FS module?"
you break this question in different questions
-What is a module in Node.js?
-What does "fs" stand for? 
-What functionalities does the fs module provide in Node.js?

You give response in array formate like this

Output: {{
"What is a module in Node.js?",
"What does "fs" stand for?",
"What functionalities does the fs module provide in Node.js?
"}}
"""
query = input("> ")
message=[{"role":"system","content":system_prompt},{"role":"user","content":query}]
question = ai(message) 

print(question)

relevent_chunk = retrieve(question)



output = answer_AI(query, relevent_chunk)

print(output)


