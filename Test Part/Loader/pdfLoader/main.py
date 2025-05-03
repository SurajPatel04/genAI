from langchain_community.document_loaders import PyPDFLoader, pdf
from pathlib import Path

pdf_path = Path(__file__).parent/"nodejs.pdf"

loader = PyPDFLoader(pdf_path)
docs = loader.load()
print(docs)
