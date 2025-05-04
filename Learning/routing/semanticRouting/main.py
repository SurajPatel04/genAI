# not working need to be fix
from openai import OpenAI
import os
from dotenv import load_dotenv
import math

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define a small set of domain prototypes
domain_prompts = {
    "python": "You are a Python expert. Always answer Python-related questions in detail.",
    "java": "You are a Java expert. Always answer Java-related questions in detail."
}

# Precompute embeddings for each domain prompt
domain_embeddings = {}
for domain, prompt in domain_prompts.items():
    resp = client.embeddings.create(
        model="text-embedding-ada-002",
        input=prompt
    )
    domain_embeddings[domain] = resp.data[0].embedding

# Cosine similarity helper
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)

# Semantic routing function
def route_semantic(query: str) -> str:
    resp = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query
    )
    query_emb = resp.data[0].embedding
    # Find the domain with the highest similarity score
    best_domain = max(
        domain_embeddings.keys(),
        key=lambda d: cosine_similarity(query_emb, domain_embeddings[d])
    )
    return best_domain

# Example usage
if __name__ == "__main__":
    user_query = input("Enter your question: ")
    domain = route_semantic(user_query)
    print(f"Routed to domain: {domain}")
