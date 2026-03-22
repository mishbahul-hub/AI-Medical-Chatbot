# from langchain_core.prompts import PromptTemplate
# from langchain_classic.chains import RetrievalQA
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# import os

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# def get_llm_chain(retriever):
#     llm = ChatGroq(
#         model = "openai/gpt-oss-120b",
#         temperature = 0.7,
#         max_tokens = None
#     )

#     prompt = PromptTemplate(
#         input_variables = ["context", "question"],
#         template = """
#         you are a **MediBot**, an AI-powered medicat assistant trained to 
#         help understand medical documents and health-related questions.

#         your job is to provide accurate and concise answers based **only on the provided context and question**.
#         ---

#         **Context**:
#         {context}
        
#         **Question**:
#         {question}
        
#         ----
#         **Answer**:
#         - respond in a calm, factual and respectful tone.
#         - use simple explanations if needed.
#         - if the context doesnot contain enough information to answer, say "Sorry, I don't have enough information to answer that question.""
#         - DONOT make up facts.
#         - DONOT give nedical advice or diagnoses.
#         """
#         )
    
#     return RetrievalQA.from_chain_type(
#         llm = llm,
#         chain_type = "stuff",
#         retriever = retriever,
#         chain_type_kwargs = {"prompt": prompt},
#         return_source_documents = True
#     )

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from logger import logger
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
def get_llm_chain(retriever: BaseRetriever):
    """
    Create a RAG (Retrieval Augmented Generation) chain that combines
    retriever output with LLM to answer questions with context.
    """
    
    try:
        # Initialize the LLM
        llm = ChatGroq(
            model = "openai/gpt-oss-120b",
            max_tokens = None
     )
        
        # Define custom prompt template that includes context
        prompt_template = """You are a medical assistant. Use the provided context to answer the question accurately.
        IMPORTANT FORMATTING INSTRUCTIONS:
- Write in clear, simple language
- Use short paragraphs (2-3 sentences each)
- DO NOT use markdown formatting like **, __, ||, tables, or asterisks
- DO NOT use special characters or technical formatting
- Organize information with clear section headings using only text (no symbols)
- Use bullet points and without special characters
- Keep sentences concise and easy to understand
- make it more interatice for the user
- make to user proper gaps bewteen paragraphs and bullet points

Context:
{context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        logger.info("Creating RetrievalQA chain with custom prompt")
        
        # Create RetrievalQA chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # Stuff all documents into context
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT},
            verbose=True  # Enable verbose logging
        )
        
        logger.info("LLM chain created successfully")
        return chain
        
    except Exception as e:
        logger.exception(f"Error creating LLM chain: {e}")
        raise