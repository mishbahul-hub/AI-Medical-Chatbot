import os
import time 
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings 
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel

# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-Embedding-0.6B")
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-Embedding-0.6B")

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medical-index"

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _init_pinecone_index():
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not set")

    pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
    existing_indexes = [index.name for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=768,
            metric="cosine",
            spec=spec
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status == "Ready":
            print("Waiting for index to be ready...")
            time.sleep(5)

    return pc.Index(PINECONE_INDEX_NAME)


def load_vectorstore(uploaded_files):
    # embed_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-Embedding-0.6B")
    # embed_model = AutoModel.from_pretrained("BAAI/llm-embedder")
    # embed_model = HuggingFaceEmbeddings(model_name="BAAI/llm-embedder")
    embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",output_dimensionality=768)
    file_paths = []
    
    # 1.  upload files 
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(save_path)

    
    index = _init_pinecone_index()

    for file_path in file_paths:

        # 2. load
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        # 3. split
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)

        # 4. retrieve page_content and metadata
        texts = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        # 5 embed 
        print(f"🔍 Embedding {len(texts)} chunks...")
        embeddings = embed_model.embed_documents(texts)

        # 6. upload to pinecone
        print(f"📤 Upserting chunks to Pinecone index '{PINECONE_INDEX_NAME}'...")
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=list(zip(ids, embeddings, metadatas)))
            progress.update(len(embeddings))

        print(f"✅ Upload complete for {file_path}")