from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

system_prompt = """
You are an AI assistant who is specialized in maths.
For the given user input, analyse the input and break it down step by step.
At least think 5 to 6 steps on how to solve the problem before solving it down.

The steps are you get user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as before giving final result.

Follow the steps in sequence: "analyse", "think", "output", "validate", and finally "result".

Rules:
1. Follow the strict JSON output as per output schema.
2. Always perform one step at a time and wait for next input.
3. Carefully analyse the user query.

Output format: 
{ "step": "string", "content": "string" }

Example:
Input: What is 2 + 2.
Output: { "step": "analyse", "content": "Alright! The user is interested in maths query and is asking a basic arithmetic operation" }
Output: { "step": "think", "content": "To perform the addition I must go from left to right and add all the operands" }
Output: { "step": "output", "content": "4" }
Output: { "step": "validate", "content": "Seems like 4 is correct answer for 2 + 2" }
Output: { "step": "result", "content": "2 + 2 = 4 and that is calculated by adding all numbers" }
"""

query = input(">> ")

message = [{"role": "system", "content": system_prompt}]
message.append({"role": "user", "content": query})

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

while True:
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        response_format={"type":"json_object"},
        messages=message
    )

    parsed_response = json.loads(response.choices[0].message.content)
    message.append({"role": "assistant", "content": json.dumps(parsed_response)})

    if parsed_response.get("step") != "output":
        print(f"🧠: {parsed_response.get('content')}")
        continue

    print(f"🤖: {parsed_response.get('content')}")
    break
