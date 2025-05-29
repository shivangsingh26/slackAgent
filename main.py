import os
from fastapi import FastAPI
from dotenv import load_dotenv
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
    VectorStoreIndex,
    SimpleDirectoryReader,
)

# -----------------------------------------------------------------------------
# Description of imported libraries:
# -----------------------------------------------------------------------------
# - SimpleDirectoryReader: Reads files from a directory.
# - VectorStoreIndex: Maintains indices for document retrieval.
# - StorageContext: Manages the storage of indexed data in the vector DB.
# - load_index_from_storage: Loads a vector index from the given storage context.

# -----------------------------------------------------------------------------
# Load environment variables and OpenAI key
# -----------------------------------------------------------------------------
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# -----------------------------------------------------------------------------
# FastAPI initialization
# -----------------------------------------------------------------------------
app = FastAPI()

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")

# -----------------------------------------------------------------------------
# Load vector index from storage
# -----------------------------------------------------------------------------
storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------
@app.get("/")
async def root():
    """
    Root endpoint to check if the Slack Agent is running.
    """
    return {"message": "Our Slack Agent is up and running!"}


@app.get("/query")
async def query_documents(question: str):
    """
    Endpoint to query the indexed documents using a vector store.
    """
    if not question.strip():
        return {"error": "Question cannot be empty."}

    try:
        response = query_engine.query(question)
        return {"response": str(response)}
    except Exception as e:
        return {"error": f"An error occurred while querying: {str(e)}"}