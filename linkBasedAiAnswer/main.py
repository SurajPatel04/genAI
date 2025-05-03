from openai import OpenAI
import os
from dotenv import load_dotenv
from loader import oneLinkRead
from ret import getChunks  
load_dotenv()
import json

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def readLinks(data):
    arr = data.split(",")
    MethodName = arr[0].strip()
    url = arr[1].strip()
    if MethodName == "oneLinkRead":
        result = oneLinkRead(url)
        return result

def getData(query):
    result = getChunks(query)
    return result

avilable_tool = {
    "readLinks":{
        "fn":readLinks,
        "description": "This function takes MethodName and the url as a input and return the output"
    },
    "getData":{
        "fn":getData,
        "description": "This function takes user query and return the relevant chunks"
    }
}

system_prompt = """

    You are an helpful AI assistant who is specializing in resolving user query.
    you work on start , plan , action , observe mode.
    for the given user query and available tools , plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    wait for the observation and based on the observation from the tool call resolve the user query.
    
    
    Rules:
    1. Follow the JSON string fromate 
    2. Always perform one step at a time and wait for next input
    3. Carefully analyse the user query
    
    
    Output JSON Format:
    {{
        "step": "string", 
        "content": "string" 
        "function": "The name of function if the step is action",
        "input": "The input patameter for the function",
    }}
    
    Available Tools:    
    readLinks = "This function takes MethodName and the url as a input and return the output"
    getData = "This function takes user query and return the relevant chunks" 


    Example:
    User Query : Read this links https://chaidocs.vercel.app/youtube/chai-aur-sql/introduction/ and tell me what is PostgresSQL
    Output :{{"step": "plan", "content": "The user is inetersted in read the links and then tell me about the PostgresSQL"}}
    Output :{{"step": "plan", "content": "From the availabe tools i should call readLinks."}}
    Output :{{"step": "action", "function": "readLinks", "input":"oneLinkRead, url"}}
    Output :{{"step": "observe", "output": "Links is stored in the data"}}
    Output :{{"step": "plan", "content": "From the availabe tools i should call getData."}}
    Output :{{"step": "action", "function": "readLinks", "input":"what is PostgresSQL:"}} 
    Output :{{"step": "observe", "output": "Here you will get some chunks"}}
    Output :{{"step": "output", "content": "From the chunks you receive give answer and in the end also give source link"}}

"""

message = [{"role":"system","content":system_prompt}] 
query = input(">>  ")
message.append({"role":"user","content":query})

while True:
    response = client.chat.completions.create(
        model = "gemini-2.0-flash",
        response_format={"type":"json_object"},
        messages = message 
    )

    parsed_output = json.loads(response.choices[0].message.content)
    message.append({"role":"assistant","content":json.dumps(parsed_output)})
    if parsed_output.get("step") == "plan":
        print("Thinking: ",parsed_output.get("content"))
        continue
    
    if parsed_output.get("step")=="action":
        print(parsed_output.get("content"))
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")

        if avilable_tool.get(tool_name, False) != False:
            output = avilable_tool[tool_name].get("fn")(tool_input)
            message.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
            continue

    if parsed_output.get("step") == "output":
        print(f"\n\nLLM Answer\n\n🤖: {parsed_output.get("content")}")
        break
