from dotenv import load_dotenv
import os

load_dotenv()
token=os.getenv("HF_TOKEN")
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Embedding Model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# DB path
PERSIST_DIRECTORY = "./chroma_db"

def create_vector_db(chunks):
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )

    vectordb.add_texts(chunks)

    return vectordb


def load_vector_db():
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )

    return vectordb