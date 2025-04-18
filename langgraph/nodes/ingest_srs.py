# import things from langchain
# import os for managing file paths
import os

# import document_loaders for loading text and PDFs
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader

#import text_splitter for splitting large texts into smaller chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

#import vectorstore for storing and retrieving embeddings
from langchain_community.vectorstores.pgvector import PGVector

# import embeddings for converting text into numerical vectors
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# import dotenv for managing environment variables
from dotenv import load_dotenv
load_dotenv()

# Whole process starts here
def process_document(file_path:str) -> PGVector:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        loader = TextLoader(file_path, encoding='utf-8')
    elif ext == '.pdf':
        loader = PyPDFLoader(file_path)
    elif ext == '.docx':
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    # Load the document text
    document = loader.load()

    # split the document text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(document)

    # Initialize a vector store using PostgreSQL and the loaded chunks using the HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=os.getenv("COLLECTION_NAME"),
        connection_string=os.getenv("CONN_STRING"),
    )
    print("Vector store initialized successfully!")
    print(vector_store)
    return vector_store