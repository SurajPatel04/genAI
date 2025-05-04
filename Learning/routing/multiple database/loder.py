from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") 

def loader(file_name, url_link, collection_name):
    # loding
    pdf_path = Path(__file__).parent/ file_name
    loader = PyPDFLoader(pdf_path)
    doc = loader.load()

    # spliting
    text_split = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_doc = text_split.split_documents(documents=doc)

    # embedding
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
    )

    #vector store
    vector_store = QdrantVectorStore.from_documents(
        documents=[],
        url=url_link,
        embedding=embeddings,
        collection_name=collection_name,
    )

    vector_store.add_documents(documents=split_doc)

    print(f"this collection is added {collection_name} in the port {url_link}")

loader("python.pdf","http://localhost:6333", "python")
loader("nodejs.pdf","http://localhost:6335", "node js")