# slackAgent

**slackAgent** is an AI-powered Slack bot that answers user queries by leveraging a vector database powered by **LlamaIndex** and **ChromaDB**. It integrates with the **Slack API** to handle messages in channels or DMs and uses **n8n** for workflow automation. Alternatively, it offers a **Streamlit**-based web UI for querying the same backend. The project uses **OpenAI embeddings** for intelligent document retrieval and **FastAPI** for a lightweight backend.

## Features

- **Slack Integration**: Responds to queries in Slack channels or DMs via the Slack Events API.
- **AI-Powered Search**: Uses LlamaIndex and ChromaDB to query documents converted into OpenAI embeddings.
- **Workflow Automation**: Automates query processing and response delivery with n8n workflows.
- **Alternative UI**: Provides a Streamlit-based web interface for querying without Slack.
- **Local-to-Web**: Exposes local APIs to the web using **ngrok**.

## Project Structure

- `app.py`: Loads documents, converts them to OpenAI embeddings, and stores them in ChromaDB.
- `main.py`: FastAPI backend to handle queries using the precomputed vector index.
- `.env`: Stores the OpenAI API key.
- `requirements.txt`: Lists Python dependencies (e.g., `llama-index`, `chromadb`, `fastapi`).
- `storage/`: Persists vector embeddings in ChromaDB.
- `documentation/`: Stores documents to be indexed.

## Setup Instructions

### Prerequisites
- Python 3.10
- Slack account and workspace
- n8n account
- ngrok account
- OpenAI API key

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/slackAgent.git
   cd slackAgent
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3.10 -m venv venvSlackAgent
   source venvSlackAgent/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   - Create a `.env` file in the root directory:
     ```
     OPENAI_API_KEY=your-openai-api-key
     DOCUMENTATION_DIR=./documentation
     STORAGE_DIR=./storage
     ```

5. **Add Documents**
   - Place documents in the `documentation/` directory for indexing.

6. **Generate Vector Embeddings**
   - Run `app.py` to load documents, create OpenAI embeddings, and store them in ChromaDB:
     ```bash
     python3.10 app.py
     ```

7. **Run the FastAPI Backend**
   - Start the FastAPI server to handle queries:
     ```bash
     uvicorn main:app --reload
     ```

### Slack API Setup

1. Create a Slack app at [api.slack.com](https://api.slack.com).
2. Add bot token scopes:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
3. Enable **Event Subscriptions** and paste your n8n webhook URL.
4. Subscribe to bot events:
   - `message.channels`
   - `message.im`
5. Add the bot to your Slack workspace (`slackAgent`).

### n8n Workflow Setup

1. Sign up for an [n8n account](https://n8n.io).
2. Create a workflow with the following nodes:
   - **Webhook**: Captures Slack events and handles Slack's challenge verification.
   - **Set Node**: Extracts `user_query` and `channel_id`.
   - **Cleanup Node**: Removes mentions (e.g., `@slackAgent`) from queries.
   - **HTTP Server Node**: Uses ngrok to forward queries to the FastAPI backend (`/query` endpoint).
   - **Merge Node**: Combines query data and backend response into a JSON.
   - **Slack Node**: Sends the response back to the Slack workspace.
3. Set the webhook to **"Respond to WebHook"** mode for Slack API verification, then switch to **"Immediately"**.
4. Run the workflow and test by sending a query (e.g., `@slackAgent how to install dependencies`) in Slack.

### Alternative: Streamlit UI

1. Set up an n8n workflow with:
   - **Webhook**: Passes queries from Streamlit to FastAPI.
   - **HTTP Server**: Uses ngrok to expose the local server.
   - **Respond to Webhook**: Formats and returns the response.
2. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

- **Slack**: Mention the bot in a channel or DM (e.g., `@slackAgent how to install dependencies`).
- **Streamlit**: Access the web UI, enter a query, and view the response.

## Example

Ask in Slack:
```
@slackAgent How do I install dependencies?
```
Response:
```
Run `pip install -r requirements.txt` in your virtual environment.
```

## Technical Details

- **Document Indexing** (`app.py`):
  - Uses `SimpleDirectoryReader` to load documents from `documentation/`.
  - Converts documents to OpenAI embeddings with `VectorStoreIndex`.
  - Stores embeddings in `ChromaDB` under `storage/developer_documents_collection`.

- **Query Handling** (`main.py`):
  - FastAPI backend with `/query` endpoint to process questions.
  - Loads precomputed index from `storage/` and uses `query_engine` for responses.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License