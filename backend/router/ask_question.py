# from fastapi import APIRouter, Form
# from fastapi.responses import JSONResponse
# from modules.llm import get_llm_chain
# from modules.query_handlers import query_chain
# from langchain_core.documents import Document
# from langchain_core.retrievers import BaseRetriever
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings 
# from pinecone import Pinecone
# from pydantic import Field
# from typing import Any, List, Optional
# from logger import logger
# import os
# from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
# from sentence_transformers import SentenceTransformer

# router = APIRouter()

# def extract_text_from_metadata(metadata: dict) -> str:
#     """
#     Try multiple field names to extract text content from Pinecone metadata.
#     """
#     # Common field names in order of preference
#     field_names = ["text", "content", "page_content", "body", "data", "doc", "chunk"]
    
#     for field in field_names:
#         value = metadata.get(field)
#         if value and isinstance(value, str) and len(value.strip()) > 0:
#             return value
    
#     # If no common fields found, log and return empty
#     logger.warning(f"No text content found in metadata. Available keys: {list(metadata.keys())}")
#     return ""

# @router.post("/ask/")
# async def ask_question(question: str = Form(...)):
#     try:
#         logger.info(f"user query: {question}")

#         # Embed model + Pinecone setup
#         pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
#         index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
#         embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", output_dimensionality=768)
#         embedded_query = embed_model.embed_query(question)

#         result = index.query(vector=embedded_query, top_k=3, include_metadata=True)

#         docs = []
#         for match in getattr(result, "matches", []):
#             metadata = match.get("metadata", {})
            
#             # Extract text using flexible method
#             page_content = extract_text_from_metadata(metadata)
            
#             # Only add if content exists
#             if page_content.strip():
#                 doc = Document(
#                     page_content=page_content,
#                     metadata=metadata
#                 )
#                 docs.append(doc)
#                 logger.info(f"Added document with {len(page_content)} chars")
#             else:
#                 logger.warning(f"Skipped empty document. Metadata keys: {list(metadata.keys())}")

#         # DEBUG: Check if documents have content
#         logger.info(f"Total documents retrieved: {len(docs)}")
#         for i, doc in enumerate(docs):
#             content_length = len(doc.page_content)
#             logger.info(f"Doc {i}: {content_length} chars | Source: {doc.metadata.get('source', 'N/A')}")
#             logger.info(f"Doc {i} preview: {doc.page_content[:150]}...")

#         if len(docs) == 0:
#             logger.error("NO DOCUMENTS WITH CONTENT FOUND!")
#             return JSONResponse(
#                 status_code=400, 
#                 content={
#                     "error": "No valid documents retrieved from Pinecone. Check metadata field names.",
#                     "suggestion": "Run debug_pinecone.py to inspect metadata structure"
#                 }
#             )

#         class SimpleRetriever(BaseRetriever):
#             tags: Optional[List[str]] = Field(default_factory=list)
#             metadata: Optional[dict] = Field(default_factory=dict)

#             def __init__(self, documents: List[Document]):
#                 super().__init__()
#                 self._docs = documents

#             def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
#                 logger.info(f"SimpleRetriever invoked with query: {query}")
#                 logger.info(f"Returning {len(self._docs)} documents with total content: {sum(len(d.page_content) for d in self._docs)} chars")
#                 return self._docs
            
#         retriever = SimpleRetriever(documents=docs)
        
#         # DEBUG: Test retriever directly
#         test_docs = retriever.invoke(question)
#         logger.info(f"Retriever test returned {len(test_docs)} documents")
        
#         chain = get_llm_chain(retriever)
#         logger.info("LLM chain created successfully")
        
#         result = query_chain(chain, question)
#         logger.info(f"Chain result: {result}")

#         logger.info("Query successful")
#         return result
    
#     except Exception as e:
#         logger.exception("Error Processing question")
#         return JSONResponse(status_code=500, content={"error": str(e)})

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
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
from sentence_transformers import SentenceTransformer

router = APIRouter()

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")

        # Embed model + Pinecone setup
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
        embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", output_dimensionality=768)
        embedded_query = embed_model.embed_query(question)

        result = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            ) for match in getattr(result, "matches",[])
        ]

        # DEBUG: Check if documents have content
        logger.info(f"Total documents retrieved: {len(docs)}")
        for i, doc in enumerate(docs):
            content_length = len(doc.page_content)
            logger.info(f"Doc {i}: {content_length} chars | Source: {doc.metadata.get('source', 'N/A')}")
            if content_length == 0:
                logger.warning(f"Doc {i} has EMPTY content!")
            else:
                logger.info(f"Doc {i} preview: {doc.page_content[:100]}...")

        class SimpleRetriever(BaseRetriever):
            tags: Optional[List[str]] = Field(default_factory=list)
            metadata: Optional[dict] = Field(default_factory=dict)

            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents

            def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
                logger.info(f"SimpleRetriever invoked with query: {query}")
                logger.info(f"Returning {len(self._docs)} documents")
                return self._docs
            
        retriever = SimpleRetriever(documents=docs)
        
        # DEBUG: Test retriever directly
        test_docs = retriever.invoke(question)
        logger.info(f"Retriever test returned {len(test_docs)} documents")
        
        chain = get_llm_chain(retriever)
        logger.info("LLM chain created successfully")
        
        result = query_chain(chain, question)
        logger.info(f"Chain result: {result}")

        logger.info("Query successful")
        return result
    
    except Exception as e:
        logger.exception("Error Processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})