#This code is for a FastAPI Backend

from fastapi import FastAPI
from dotenv import load_dotenv
import os
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

## A little about the imported libraries......
#SimpleDirectoryReader ----> Helps to read text directory from files from a directory
#VectorStoreIndex ---------> Maintains indices for document retrieval
#StorageContext -----------> Manages storage of the indexed data present in the vectorDB
#load_index_from_storage --> Loads the vector index from the storage context

load_dotenv()
#load OPENAI KEY
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#Initalize FastAPI app
app = FastAPI()

#Load precomputed index from storage
storage_context = StorageContext.from_defaults(persist_dir="./storage")

#consists of the vector embeddings of the documents
index = load_index_from_storage(storage_context)

#Create a query engine to handle queries against the index
query_engine = index.as_query_engine()

@app.get("/")
async def root():
    """
    Root endpoint to check if the Slack Agent is running.
    """
    return {"message": "Our Slack Agent is up and running!"}

@app.get("/query")
async def query_documents(question: str):
    """
    Endpoint to query the indexed documents.
    """
    if not question.strip():
        return {"error": "Question cannot be empty."}

    try:
        response = query_engine.query(question)  # Use pre-created query_engine
        return {"response": str(response)}
    except Exception as e:
        return {"error": f"An error occurred while querying: {str(e)}"}