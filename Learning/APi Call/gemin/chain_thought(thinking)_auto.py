from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv


load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

system_prompt = """
you are an ai assistant who is specialized in maths.
For the given user input, analyse the input and break it down step by step
At least think 5 to 6 steps on how to solve the problem before solving it down.

The steps are you get user input, you analyse, you think , you again think for several times and then return an output with explanation and then finally you validate the output as before giving final result

Follow the steps in sequence  that is "analyse", "think", "output", "validate" and finally "result"

Rules:
1. Follw the strict json output as per output schema
2. Always perform one step at a time and waint for next input
3. Creafully analyse the user query

Output format: 
{{ step: "string", content: "string"}}

Example:
Input: What is 2 + 2.
Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}

"""

message = [f"""role: system, content: {system_prompt}"""]

query = input(">>>")
message.append(f"""role: user, content: {query}""")
print(message)
print(type(message))
hold = []
while(True):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents = message,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )

    parsed_response = json.loads(response.text)
    hold = message.copy()
    message.clear()

    hold.append(json.dumps({"role": "assistant", "content": parsed_response}))
    print("\n\nhold part ",hold)



    if parsed_response.get("step") != "output":
        print(f"🧠: {parsed_response.get("content")}")
        message.clear()
        message = hold.copy()
        hold.clear()
        print("\n\nmessage part: ",message)
        print("\n\nagain hold part ",hold)
        continue
    

    print(f"🤖 {parsed_response.get("output")}")
    break