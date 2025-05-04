from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def choose_model(prompt: str) -> str:
    """
    Simple rule-based router:
     - Code questions → gpt-4-code
     - Short prompts (<200 chars) → gpt-3.5-turbo
     - Everything else → gpt-4
    """
    lower = prompt.lower()
    if any(k in lower for k in ("python", "javascript", "code")):
        return "gpt-4-code"
    if len(prompt) < 200:
        return "gpt-3.5-turbo"
    return "gpt-4"

def chat_with_user(prompt: str) -> str:
    model = choose_model(prompt)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_input = input("You: ")
    answer = chat_with_user(user_input)
    print(f"AI ({choose_model(user_input)}): {answer}")
