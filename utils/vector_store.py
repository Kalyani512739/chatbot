from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from google import genai
import os
import uuid

# -----------------------------------
# Load Environment Variables
# -----------------------------------

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# -----------------------------------
# Gemini Client
# -----------------------------------

client = genai.Client(
    api_key=GOOGLE_API_KEY
)

# -----------------------------------
# Pinecone Setup
# -----------------------------------

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

INDEX_NAME = "chatbot-index"

# -----------------------------------
# Create Index If Not Exists
# -----------------------------------

existing_indexes = pc.list_indexes().names()

if INDEX_NAME not in existing_indexes:

    pc.create_index(
        name=INDEX_NAME,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to index
index = pc.Index(INDEX_NAME)

# -----------------------------------
# Generate Gemini Embeddings
# -----------------------------------

def get_embedding(text):

    if not text.strip():
        text = "empty"

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values

# -----------------------------------
# Store Chunks In Pinecone
# -----------------------------------

def create_vector_db(chunks):

    vectors = []

    for chunk in chunks:

        embedding = get_embedding(chunk)

        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {
                "text": chunk
            }
        })

    # Upload vectors correctly
    index.upsert(
        vectors=vectors
    )

    print("Vectors uploaded to Pinecone 😎")

# -----------------------------------
# Search Similar Chunks
# -----------------------------------

def search_chunks(query, top_k=4):

    query_embedding = get_embedding(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results["matches"]