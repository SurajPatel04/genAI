from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

text = "Eiffel Tower is in Paris and is a famous landmark, it is 324 meters tall"

respose = client.embeddings.create(
    input = text,
    model = "text-embedding-3-small"
)
