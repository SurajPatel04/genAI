from langchain_core.utils.html import extract_sub_links
from langchain_community.document_loaders import WebBaseLoader, web_base
import requests


def linkLoader(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    print(docs)

url="https://chaidocs.vercel.app/youtube/chai-aur-sql/welcome/"
response = requests.get(url)
content = response.text

links = extract_sub_links(content, url=url, prevent_outside=False)

for link in links:
    print(link)
