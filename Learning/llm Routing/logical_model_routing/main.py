from openai import OpenAI
import os
from dotenv import load_dotenv
from modelRouting.logical_model_routing.gemini_2_0 import gemini2_0
from modelRouting.logical_model_routing.gemini_1_5 import gemini1_5
import json

load_dotenv()

def ai_model(all):
    array = all.split(",")
    query =array[0].strip()
    model=array[1].strip()

    if model == "2.0":
        print("\nGemini Model 2.0\n")
        data = gemini2_0(query)
        print(data)
    if model == "2.5":
        print("\nGemini Model 2.5\n")
        data = gemini1_5(query)
        print(data)
    

tools = {
    "ai_model":{
        "fn":ai_model,
        "description":"This function takes user_query,model name as input and print the similar chunk"
    }
}

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.

    Note: 
    You have two model one is gemini 2.0 and another one is 2.5 
    2.0 model is good for python
    2.5 model is good for the javascript

    tools:
    ai_model: "This function takes user_query,model name as input and print the similar chunk"
    Example: 
User query: What is fs module?
Output: {{"step":"plan","content":"The user is interested to know the What is fs module?"}}
Output: {{"step":"plan","content":"From the avilable tool i need call ai_model based on the user query"}}
Output: {{"step":"action","function":"ai_model","input": "What is fs module? , 2.0}}

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
            break