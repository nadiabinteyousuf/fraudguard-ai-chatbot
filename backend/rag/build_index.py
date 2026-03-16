import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.rag.vector_store import create_vector_store
from backend.config import DATA_PATH

if __name__ == "__main__":
    file_path = os.path.join(DATA_PATH, "aml_notes.txt")
    create_vector_store(file_path)
    print("FAISS index created successfully.")
