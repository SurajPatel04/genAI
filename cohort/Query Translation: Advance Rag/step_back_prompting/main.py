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
    )
    return response.choices[0].message.content


client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
system_prompt = f"""
You are an expert at node js knowledge. 
Your task is to step back and paraphrase a question to a more generic 
step-back question, which is easier to answer. 

RESPONSE FORMAT (Strictly follow this structure):
User Question: <repeat the original question here>
<write the generalized, step-back question here>

Here are a few examples:
Original Question: Which version of Node.js introduced the `fs.promises` API?
Stepback Question: What are the key features introduced in different versions of Node.js?

Original Question: How do you handle streams in the `fs` module for large file uploads?
Stepback Question: How does the `fs` module handle file streams in Node.js?

Original Question: Which core module in Node.js supports HTTP server creation?
Stepback Question: What are the core modules provided by Node.js and their functionalities?

Original Question: How does the `cluster` module help improve performance on multi-core systems?
Stepback Question: What is the purpose of the `cluster` module in Node.js?

Response Formate should be like this
User Question: Which core module in Node.js supports HTTP server creation?
Output: What are the core modules provided by Node.js and their functionalities? 
"""
query = input("> ")
message=[{"role":"system","content":system_prompt},{"role":"user","content":query}]
question = ai(message) 

print("Step Back Question: ")
print(question)

relevant_chunk = retrieve(question)

llm_output = answer_AI(query, relevant_chunk)

print("\n------------------")
print("Answer: ")
print(llm_output)



