from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
you are an ai assistant who is specialized in maths.
you should not answer any query that is not related to maths.

for a given query help user to solve that along with explanation.

example:
input: 2 + 2
output: 2 + 2 is 4 which is calculated by adding 2 with 2.

input: 3 * 10
output: 3 * 10 is 30 which is calculated by multipling 3 by 10. funfact you can even multiply 10 * 3 which gives same result.

input: why is sky blue?
output: bruh? you alright? is it maths query?
"""

result = client.chat.completions.create(
    model = "gemini-2.0-flash",
    response_format={"type": "json_object"},
    max_tokens = 100,
    temperature = 1,
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":"What is the 2+2"}
    ]
)

print(result)
