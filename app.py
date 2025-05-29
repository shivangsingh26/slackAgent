import os
from dotenv import load_dotenv
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# -----------------------------------------------------------------------------
# Explanation of Libraries
# -----------------------------------------------------------------------------
# SimpleDirectoryReader ---> Helps read files from a directory
# VectorStoreIndex --------> Maintains indices for document retrieval
# StorageContext ----------> Manages storage of the indexed data in the vector DB
# ChromaVectorStore -------> Enables use of ChromaDB as our vector DB
# chromadb ----------------> Lightweight open-source vector database

# -----------------------------------------------------------------------------
# Load environment variables and OPENAI key
# -----------------------------------------------------------------------------
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# -----------------------------------------------------------------------------
# Directory setup and checks
# -----------------------------------------------------------------------------
# Get directory paths from environment variables or use defaults
DOCUMENTATION_DIR = os.getenv("DOCUMENTATION_DIR", "./documentation")
STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")

# Ensure required directories exist
if not os.path.exists(DOCUMENTATION_DIR):
    os.makedirs(DOCUMENTATION_DIR)
    print(f"Created missing directory: {DOCUMENTATION_DIR}")

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)
    print(f"Created missing directory: {STORAGE_DIR}")

# Check if documentation directory is empty
if not os.listdir(DOCUMENTATION_DIR):
    raise Exception(
        f"The {DOCUMENTATION_DIR} directory is empty. Please add documents to proceed."
    )

# -----------------------------------------------------------------------------
# Load documents and initialize ChromaDB
# -----------------------------------------------------------------------------
documents = SimpleDirectoryReader(DOCUMENTATION_DIR).load_data()

# Initialize ChromaDB with persistent storage
chroma_client = chromadb.PersistentClient(path=STORAGE_DIR)

# Set collection name
COLLECTION_NAME = "developer_documents_collection"

# Try to get or create the ChromaDB collection
try:
    chroma_collection = chroma_client.get_collection(COLLECTION_NAME)
except Exception:
    chroma_collection = chroma_client.create_collection(COLLECTION_NAME)

# Wrap ChromaDB collection as a vector store
vector_store = ChromaVectorStore(chroma_collection)

# -----------------------------------------------------------------------------
# Create vector index and persist it
# -----------------------------------------------------------------------------
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)

# Save vector embeddings
index.storage_context.persist(persist_dir=STORAGE_DIR)

print("Lessgooo, Documents Loaded successfully")