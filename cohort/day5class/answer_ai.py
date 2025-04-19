from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


cclient = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)
