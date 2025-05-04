from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))



response = client.models.generate_content(
    model = "gemini-2.0-flash-001",
    contents = "what is 2+2"

) 
print(response)
print(response.text)

 
