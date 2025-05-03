from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY =os.getenv("GOOGLE_API_KEY")
QUADRANT_HOST = "localhost"
NEO4J_URL ="bolt://localhost:7687"
NEO4J_USERNAME ="neo4j"
NEO4J_PASSWORD = "raja12345"

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GOOGLE_API_KEY,
            "model": "models/gemini-embedding-exp-03-07",
            "embedding_dims": 1536,
        },
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GOOGLE_API_KEY,
            "model": "gemini-1.5-flash-latest"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QUADRANT_HOST,
            "port": 6333,
            # make sure your Qdrant collection uses 1536-dim vectors
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URL,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD
        }
    }
}

mem_client = Memory.from_config(config)
client = OpenAI (
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def chat(message):

    mem_result = mem_client.search(query=message, user_id="s2004")

    memories = "\n".join([m["memory"] for m in mem_result.get("results")])

    SYSTEM_PROMPT=f"""
        You are a Memory-Aware Fact Extraction Agent, an advanced AI designed to
        systematically analyze input content, extract structured knowledge, and maintain an
        optimized memory store. Your primary function is information distillation
        and knowledge preservation with contextual awareness.

        Tone: Professional analytical, precision-focused, with clear uncertainty signaling
        
        Memory and Score:
        {memories}
    """

    message = [
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":message}
    ]

    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=message,
    )
    message.append(
        {"role":"assistant","content":response.choices[0].message.content}
    )


    #This line will add the message to the neo4j and qdrant
    #here user id is hard writen but in the future we take this id from the user database
    # mem_client.add(message, user_id="s2004")


    return response.choices[0].message.content

while True:
    message = input("> ")
    print("BOT: ", chat(message=message))