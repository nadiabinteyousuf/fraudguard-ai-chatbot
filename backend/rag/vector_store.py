import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import FAISS_INDEX_PATH

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_FILE = os.path.join(BASE_DIR, "data", "aml_notes.txt")
DB_PATH = os.path.join(BASE_DIR, FAISS_INDEX_PATH)


def create_vector_store(file_path: str):
    print("Loading file from:", file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    loader = TextLoader(file_path, encoding="utf-8", autodetect_encoding=True)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(DB_PATH)

    return vectorstore


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if not os.path.exists(DB_PATH):
        return create_vector_store(DATA_FILE)

    return FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )