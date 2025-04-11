import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the GenAI client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model instance
model = genai.GenerativeModel(model_name='gemini-2.0-flash-001')

# Define a role-based prefix
role_prompt = """When user ask question then give me response in the form of json 
Example
User: What is the 2+2
Response{
Output: "2+2 is 4"

Example:
User: Hello
Response {
output: Your response here
}
}
"""

# Get user input
user_input = input("Enter a input: ")

# Combine role prompt with user query
full_prompt = f"{role_prompt}\n\nUser Query: {user_input}"

# Generate content using the role-based prompt
response = model.generate_content(full_prompt)

# Print the response
print("\nModel Response:")
print(response.text)

