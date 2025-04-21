from typing import Li, Tuple, Dict
import os

from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def reciprocal_rank_fusion(rankings, k = 15):
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
    # return list of (doc_id, score) sorted by score desc
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def retrieve(queries,k=15):
    # 1) ensure key
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

    # 2) init embedding + Qdrant client & store
    embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    relevent_chunk = QdrantVectorStore.from_existing_collection(
        collection_name="parallel_query",
        embedding=embedding,
        url="http://localhost:6333",
    )

    # 3) run each sub‑query, collect rankings of IDs + keep lookup
    rankings = []
    lookup= {}

    for q in queries:
        docs = relevent_chunk.similarity_search(query=q, k=k)
        ids = []
        for d in docs:
            # assume each Doc has a unique metadata["id"]
            doc_id = d.metadata.get("id") or f"{d.metadata.get('page')}#{hash(d.page_content)}"
            ids.append(doc_id)
            lookup[doc_id] = d
        rankings.append(ids)

    # 4) fuse the ranked ID lists
    fused = reciprocal_rank_fusion(rankings)

    # 5) map fused IDs back to Doc objects, preserving order
    fused_docs = []
    for doc_id, score in fused:
        if doc_id in lookup:
            fused_docs.append(lookup[doc_id])


    # 6) format into your final context string
    formatted = []
    for doc in fused_docs:
        page = doc.metadata.get("page", "?")
        text = doc.page_content.strip()
        formatted.append(f"[Page {page}]\n{text}")
    
    print(formatted)
    return "\n\n".join(formatted)

