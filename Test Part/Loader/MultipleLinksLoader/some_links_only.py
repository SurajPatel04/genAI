from langchain_core.utils.html import extract_sub_links
from langchain_community.document_loaders import WebBaseLoader, web_base
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def linkLoader(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    print(docs)

def linkExtract(url):
    url="https://docs.chaicode.com/youtube/chai-aur-django/welcome/"
    response = requests.get(url)
    content = response.text

    links = extract_sub_links(content, url=url, prevent_outside=False)
    str = ""
    for link in links:
        str += link + "\n"



avilable_tool = {
    "linkExtract":{
        "fn":linkExtract,
        "description": "This is extract sub links"
    }
}


system_propmpt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

     
    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - linkExtract: "This is extract sub links"i

    Example how to return link
    User query:  https://docs.chaicode.com/youtube/chai-aur-django/welcome/ 
    
    After extraction you will get so many links
    https://docs.chaicode.com/youtube/chai-aur-git/behind-the-scenes/
https://docs.chaicode.com/youtube/chai-aur-sql/introduction/
https://docs.chaicode.com/youtube/chai-aur-devops/postgresql-vps/
https://www.youtube.com/@chaiaurcode
https://docs.chaicode.com/youtube/chai-aur-c/control-flow/
https://docs.chaicode.com/youtube/chai-aur-devops/node-nginx-vps/
https://docs.chaicode.com/youtube/chai-aur-django/getting-started/
https://docs.chaicode.com/youtube/chai-aur-git/branches/
https://docs.chaicode.com/youtube/chai-aur-sql/joins-and-keys/
https://docs.chaicode.com/youtube/chai-aur-c/introduction/
https://docs.chaicode.com/youtube/chai-aur-devops/nginx-rate-limiting/
https://docs.chaicode.com/youtube/chai-aur-sql/welcome/
https://docs.chaicode.com/youtube/chai-aur-c/data-types/
https://docs.chaicode.com/youtube/chai-aur-django/relationships-and-forms/
https://docs.chaicode.com/youtube/chai-aur-django/welcome/

You then observe the link and in the final answer you will only send the links that has most comman 


Example: 
User query:  https://docs.chaicode.com/youtube/chai-aur-django/welcome/ 
Output: {{"step":"plan","content":"The user is wanted to extract this links}}
Output: {{"step":"plan","content":"From the avilable tool i need call linkExtract }}

Output: {{"step":"action","function":"linkExtract","input":"https://docs.chaicode.com/youtube/chai-aur-django/welcome"}}
Output: {{"step":"observe","output":"You get so many links"}}
Output: {{"step":"output","content":"In observe you have so many links and user links has chai-aur-django parts so output should be all that links that is related to the chai-aur-django}}

"""

query = input(">> ")

message = [{"role": "system", "content": system_propmpt}]
message.append({"role": "user", "content": query})

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
        
        if avilable_tool.get(tool_name, False) != False:
            output = avilable_tool[tool_name].get("fn")(tool_input)
            message.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
            continue

    if parsed_output.get("step") == "output":
        print(f"🤖: {parsed_output.get("content")}")
        break
