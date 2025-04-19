from typing import Collection
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
pdf_path = Path(__file__).parent/ "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
doc = loader.load()

text_spliters = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
) 
split_doc = text_spliters.split_documents(documents=doc)

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

embedding = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

vector_store=QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    embedding=embedding,
    collection_name="parallel_query",
)

vector_store.add_documents(documents=split_doc)

retrive = QdrantVectorStore.from_existing_collection(
    collection_name = "parallel_query",
    embedding=embedding,
    url="http://localhost:6333",
)

relevent_chunk = retrive.similarity_search(
    query="What is FS Module",
)

formatted = []

for doc in relevent_chunk:
    snippet = f"[Page {doc.metadata.get('page')}] \n{doc.page_content}"
    formatted.append(snippet)

context = "\n\n".join(formatted)


print(formatted)

