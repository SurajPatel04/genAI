from langchain_core.utils.html import extract_sub_links
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
import requests


load_dotenv()



def oneLinkRead(url):
    loader = WebBaseLoader(url)
    docs = loader.load()

    split_text = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    split_doc = split_text.split_documents(documents=docs)

    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") 

    embedding = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
    )

    vector_store = QdrantVectorStore.from_documents(
        documents = [],
        url="http://localhost:6333/",
        embedding=embedding,
        collection_name="chai_code_docs"
    )

    vector_store.add_documents(documents=split_doc)

    return "Vector store is done"




