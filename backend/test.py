# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import google.generativeai as genai
# genai.configure(api_key="AIzaSyDVq6Q21XH8DO0DqAq-p3AUtTHa9dv3SOQ")
# for m in genai.list_models():
#     print(m.name, m.supported_generation_methods)
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings 
from pinecone import Pinecone
from pydantic import Field
from typing import Any, List, Optional
from logger import logger
import os



pc = Pinecone(api_key=os.environ["pcsk_2dek45_92nHibxnFPzFjXbBTxHsKMRo25y2cNku2vnWfvc5enTcX6QuLLPxD7oGHEWjA4J"])
index = pc.Index(os.environ["medical-index"])
# embed_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-Embedding-0.6B")
        # embed_model = SentenceTransformer("google/embeddinggemma-300m")
        # embed_model = AutoModel.from_pretrained("BAAI/llm-embedder")
embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", output_dimensionality=768)
embedded_query = embed_model.embed_query("what is diabetes?")


result = index.query(vector=embedded_query, top_k=3, include_metadata=True)

docs = []

for match in getattr(result, "matches", []):
        
        metadata = getattr(match, "metadata", {}) or {}
        text = metadata.get("text", "")

        docs.append(
            Document(
                page_content=text,
                metadata=metadata
                )
            )
        
for match in getattr(result, "matches", []):
    print(match.metadata)