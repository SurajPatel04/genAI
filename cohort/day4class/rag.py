
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings


from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") 


""" here (__file__).parent meanse current dir mai hai file """
pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
doc = loader.load()


""" chunk_overlap means it has some previouse chunk part also """
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

split_doc = text_spliter.split_documents(documents=doc)
    

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
)

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     embedding=embeddings,
#     collection_name="learning_langchain"
# )

# vector_store.add_documents(documents=split_doc)

""" print("Injection Done") """


retriver = QdrantVectorStore.from_existing_collection(
    collection_name = "learning_langchain",
    embedding=embeddings,
    url="http://localhost:6333"
)

relevent_chunk = retriver.similarity_search(
    query="What is FS Module",

)

""" print(relevent_chunk) """

formated = []

for doc in relevent_chunk:
    snippet = f"[Page {doc.metadata.get('page')}] \n{doc.page_content}"
    formated.append(snippet)

context = "\n\n".join(formated)

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

SYSTEM_PROMPT = """
You are an helpfull AI Assiatant who responds base of the avilable context.

Context: 
{context}
"""

message = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":"What is FS Module"}]

response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type":"json_object"},
            messages = message
    )

print(response.choices[0].message.content)
