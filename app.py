import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

## A little about the imported libraries......
#SimpleDirectoryReader ----> Helps to read text directory from files from a directory
#VectorStoreIndex ---------> Maintains indices for document retrieval
#StorageContext -----------> Manages storage of the indexed data present in the vectorDB

#ChromaVectorStore --------> Used to make sure we can use ChromaDB as our vectorDB
#chromadb -----------------> A lightweight opensource vectorDB

#Load OPENAI KEY
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

################## SOME NUNCHECKS #####################################

# Get directory paths from environment variables or use defaults
documentation_dir = os.getenv("DOCUMENTATION_DIR", "./documentation")
storage_dir = os.getenv("STORAGE_DIR", "./storage")

# Ensure directories exist
if not os.path.exists(documentation_dir):
    os.makedirs(documentation_dir)
    print(f"Created missing directory: {documentation_dir}")

if not os.path.exists(storage_dir):
    os.makedirs(storage_dir)
    print(f"Created missing directory: {storage_dir}")

# Check if documentation directory is empty
if not os.listdir(documentation_dir):
    raise Exception(f"The {documentation_dir} directory is empty. Please add documents to proceed.")

#########################################################################

#Load our documents
documents = SimpleDirectoryReader(documentation_dir).load_data()

#Initialize ChromaDB, define a storage dir to persist our data
chroma_client = chromadb.PersistentClient(path=storage_dir)

#Load chroma collection
collection_name = "developer_documents_collection"

#Look for collection with name given above, 
#if it doesnt exists, create a new one.
try:
    chroma_collection = chroma_client.get_collection(collection_name)

except Exception:
    chroma_collection = chroma_client.create_collection(collection_name)

#Wrap chromaDB as vector store
vector_store = ChromaVectorStore(chroma_collection)

#Now lets create Vector Index(converting documents into OPENAI Embeddings)
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)

#Now storing our vector embeddings inside our persisted folder
index.storage_context.persist(persist_dir=storage_dir)

print("Lessgooo, Documents Loaded successfully")