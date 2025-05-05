from qdrant_client import QdrantClient
from langchain_openai import AzureOpenAIEmbeddings
from qdrant_client.http.models import Distance, VectorParams
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Initialize AzureOpenAIEmbeddings
embeddings = AzureOpenAIEmbeddings(
    model=os.getenv('AZURE_OPENAI_EMBEDDING_MODEL'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    azure_endpoint=os.getenv('AZURE_OPENAI_API_URL'),
    openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION')
)

# Initialize Qdrant Client
qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_FULL_ACCESS_KEY')
client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)

# Prepare your data
collection_name = "workarounds"
corpus = pd.read_csv('workarounds_corpus.csv')

# Ensure your collection exists, create if it doesn't
try:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )
except Exception as e:
    print(f"Collection may already exist: {e}")

# Generate embeddings for all documents
document_texts = corpus['Workaround im Story Format'].tolist()
reference_ids = corpus['ID'].tolist()

# Get embeddings using embed_documents
embeddings_vectors = embeddings.embed_documents(document_texts)

# Prepare documents for upsert into Qdrant using unsigned integers for IDs
documents = [
    {"id": i, "vector": vector, "payload": {"page_content": text, "reference_id":reference_id}}
    for i, (reference_id, vector, text) in enumerate(zip(reference_ids, embeddings_vectors, document_texts ), start=1)  # Start id from 1
]

# Upsert the documents into the Qdrant collection
client.upsert(
    collection_name=collection_name,
    points=documents
)

print("Documents inserted successfully.")