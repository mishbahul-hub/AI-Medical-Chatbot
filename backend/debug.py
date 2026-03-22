from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
import os
import json
 
# Setup
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ["PINECONE_INDEX_NAME"])
embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", output_dimensionality=768)
 
# Sample question
question = "what is diabetes"
embedded_query = embed_model.embed_query(question)
 
# Query Pinecone
result = index.query(vector=embedded_query, top_k=3, include_metadata=True)
 
print("\n" + "="*80)
print("PINECONE METADATA DEBUG")
print("="*80)
 
for i, match in enumerate(getattr(result, "matches", [])):
    print(f"\n--- MATCH {i} ---")
    print(f"Match ID: {match.get('id', 'N/A')}")
    print(f"Score: {match.get('score', 'N/A')}")
    
    metadata = match.get("metadata", {})
    print(f"\nMetadata Keys: {list(metadata.keys())}")
    
    print(f"\nFull Metadata:")
    for key, value in metadata.items():
        value_preview = str(value)[:100]
        print(f"  {key}: {value_preview}...")
    
    # Check common field names
    print(f"\nField Length Check:")
    for field in ["text", "content", "page_content", "body", "data", "doc"]:
        value = metadata.get(field, "NOT FOUND")
        if value != "NOT FOUND":
            print(f"  {field}: {len(str(value))} chars")
        else:
            print(f"  {field}: NOT FOUND")
 
print("\n" + "="*80)