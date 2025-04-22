from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

def retrieve(query) -> str:
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


    embedding = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )


    retrive = QdrantVectorStore.from_existing_collection(
        collection_name = "parallel_query",
        embedding=embedding,
        url="http://localhost:6333",
    )

    relevant_chunks = retrive.similarity_search(
        query=query,
    )


    for doc in relevant_chunks:
        print("-------------------------")
        print("Page Content: ", doc.page_content)
        print("Page Number: ", doc.metadata.get("page"))
        print("-------------------------")

