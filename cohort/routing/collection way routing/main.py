from openai import OpenAI
import os
from dotenv import load_dotenv
from retrieval import retrieve
import json

load_dotenv()

def ret(all):
    arr = all.split(",")
    query=arr[0].strip()
    collection_name=arr[1].strip()
    print(all)
    data=retrieve(query, collection_name)
    return data

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

tools = {
    "ret":{
        "fn":ret,
        "description":"This function takes user_query, collection_name, url as input and print the similar chunk"
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.

    Note:
    Answer should be in detail
    You recive a question and you give answer based on the assistant content and 
    also Mention the page number from where did you pick all the information and
    If you add something from you then tell where did you added something

    collections:
    {{collection_name: python,
    collection_name: node js
       }}
    

    Available Tools: 
    "ret":"This function takes user_query, collection_name, url as input and print the similar chunk"

    In ret you need to pass the user_query, collection_name and url and you choose right collection_name and the right url

    Example: 
User query: What is fs module?
Output: {{"step":"plan","content":"The user is interested to know the What is fs module?"}}
Output: {{"step":"plan","content":"From the avilable tool i need call ret or other tool that give me expected output"}}
Output: {{"step":"action","function":"ret","input": "What is fs module? , node js}}
Output: {{"step":"assistant","content":"Here you get the user query chunk and based on the chunk answer the user question and in the last mention page number}}
Output: {{"step":"observe","output":"Here you get the relvant chunk of the document"}}
Output: {{"step":"output","content":"give the answer based on the relevant chunk and in the end also mention page number"}}
       """

query = input("> ")
message =[
    {"role":"system","content":system_prompt},
    {"role":"user","content":query}]

while True:
    response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type":"json_object"},
            messages = message
    )
    parsed_output = json.loads(response.choices[0].message.content)
    message.append({"role":"assistant","content":json.dumps(parsed_output)})
    if parsed_output.get("step") == "plan":
        print("Thinking: ",parsed_output.get("content"))
        continue 

    if parsed_output.get("step") == "action":
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")
        
        if tools.get(tool_name, False) != False:
            output = tools[tool_name].get("fn")(tool_input)
            message.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
            
    if parsed_output.get("step") == "output":
        print("\n\n relveant chunk with llm answer")
        print(f"🤖: {parsed_output.get("content")}")
        break