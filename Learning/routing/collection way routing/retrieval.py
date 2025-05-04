from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os


def retrieve(query, collection_name):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

    #Same database but different collection name
    retrive = QdrantVectorStore.from_existing_collection(
        collection_name = collection_name,
        embedding=embedding,
        url="http://localhost:6333",
    )

    relevent_chunk = retrive.similarity_search(
        query=query,
    )

    formatted = []

    for doc in relevent_chunk:
        snippet = f"[Page {doc.metadata.get('page')}] \n{doc.page_content}"
        formatted.append(snippet)

    context = "\n\n".join(formatted)
    return context

