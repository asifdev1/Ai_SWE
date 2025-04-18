#  function to establish the connection to the database and fetch the vectors we need

from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_vector_store():
    CONNECTION_STRING = os.getenv("CONN_STRING")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    vector_store = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        embedding_function=embedding,
    )

    return vector_store