from openai import OpenAI
import os 
from dotenv import load_dotenv
import json
import requests

load_dotenv()

def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

avaiable_tools = {
    "get_weather":{
        "fn": get_weather,
        "description": "Take a city name as input and returns the current weather for the city"
    }
}
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

system_prompt = f"""
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
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput
    
    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""
query = input(">> ")

message = [{"role": "system", "content": system_prompt}]
message.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type":"json_object"},
            messages=message
    )

    parsed_output = json.loads(response.choices[0].message.content)
    message.append({"role": "assistant", "content": json.dumps(parsed_output)})


    if parsed_output.get("step") == "plan":
        print(f"Think: {parsed_output.get("content")}")
        continue
    
    if parsed_output.get("step") == "action":
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")

        if avaiable_tools.get(tool_name, False) != False:
            output = avaiable_tools[tool_name].get("fn")(tool_input)
            message.append({"role":"assistant", "content": json.dumps({"step": "observe", "output": output})})
            continue

    if parsed_output.get("step") == "output":
        print(f"🤖: {parsed_output.get('content')}")
        break



