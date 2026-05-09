from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_db(chunks):

    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory="./chroma_db"
    )

    vectordb.persist()

    return vectordb



def load_vector_db():

    vectordb = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_model
    )

    return vectordb