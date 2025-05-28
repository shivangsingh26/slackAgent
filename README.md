# slackAgent

**slackAgent** is an AI-powered Slack bot that answers user queries by leveraging a vector database built with **LlamaIndex** and **ChromaDB**. It integrates with the **Slack API** to handle messages in channels or direct messages (DMs), uses **n8n** for workflow automation, and offers a **Streamlit**-based web UI as an alternative interface. Powered by **OpenAI embeddings** and a **FastAPI**-backend, it delivers intelligent document retrieval with a seamless user experience.

## Features

- **Slack Integration**: Responds to queries in Slack channels or DMs via the Slack Events API.
- **AI-Powered Search**: Queries documents using LlamaIndex and ChromaDB with OpenAI embeddings.
- **Workflow Automation**: Automates query processing with n8n workflows.
- **Web UI Option**: Provides a Streamlit-based interface for querying without Slack.
- **Local-to-Web**: Exposes local APIs to the web using **ngrok** for seamless integration.

## Project Structure

- `app.py`: Loads documents, generates OpenAI embeddings, and stores them in ChromaDB.
- `main.py`: FastAPI backend to handle queries using the precomputed vector index.
- `.env`: Stores OpenAI API key, documentation, and storage directories.
- `requirements.txt`: Lists dependencies (e.g., `llama-index`, `chromadb`, `fastapi`).
- `storage/`: Persists vector embeddings in ChromaDB.
- `documentation/`: Stores documents for indexing.

## Setup Instructions

### Prerequisites
- Python >= 3.9
- Slack account and workspace
- n8n account
- ngrok account
- OpenAI API key

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shivangsingh26/slackAgent.git
   cd slackAgent
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venvSlackAgent
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
   - Run `app.py` to load documents and store embeddings in ChromaDB:
     ```bash
     python3 app.py
     ```

7. **Run the FastAPI Backend**
   - Start the FastAPI server to handle queries:
     ```bash
     uvicorn main:app --reload
     ```

8. **Set Up ngrok**
   - **What is ngrok?** ngrok creates a secure public URL for your local server, enabling external services like Slack or n8n to communicate with your FastAPI backend.
   - **Why use ngrok?** It exposes your local server (e.g., `http://localhost:8000`) to the internet, necessary for Slack's Event Subscriptions and n8n workflows.
   - **Setup Steps**:
     1. Sign up for an [ngrok account](https://ngrok.com) and get your authtoken.
     2. Install ngrok and authenticate:
        ```bash
        ngrok authtoken <your-ngrok-authtoken>
        ```
     3. Run the ngrok server (default port is 8000, adjust if different):
        ```bash
        ngrok http http://localhost:8000
        ```
     4. Copy the ngrok URL (e.g., `https://<random>.ngrok.io`) for Slack and n8n configurations.

### Slack API Setup

The **Slack API** enables the bot to read and post messages, respond to user actions, and automate workflows. The **Events API** notifies the bot of events like messages or channel joins via payloads.

1. Create a Slack app at [api.slack.com](https://api.slack.com).
2. Add the following bot token scopes:
   - `app_mentions:read`: Detects when the bot is mentioned (e.g., `@slackAgent help`).
   - `channels:history`: Reads message history in public channels where the bot is a member.
   - `channels:join`: Allows the bot to join public channels.
   - `channels:read`: Accesses public channel details.
   - `chat:write`: Enables sending messages in channels and DMs.
   - `chat:write.public`: Allows sending messages in public channels without joining.
   - `commands`: Supports custom slash commands for the bot.
   - `im:history`: Reads direct message history.
   - `im:write`: Sends messages in direct message conversations.
   - `mpim:history`: Accesses message history in group DMs.
3. Enable **Event Subscriptions** and use your ngrok URL (e.g., `https://<random>.ngrok.io/slack/events`) as the webhook.
4. Subscribe to the following bot events:
   - `message.channels`: Triggers when a message is posted in a public channel the bot is in.
   - `message.im`: Triggers when a message is posted in a direct message with the bot.
5. Set up challenge verification:
   - In n8n, add a webhook node and set a challenge field to capture Slack's verification parameter.
   - Set the webhook to **"Respond to WebHook"** mode for verification, then switch to **"Immediately"** after.
6. Add the bot (`slackAgentApp`) to your Slack workspace.

### n8n Workflow Setup

1. Sign up for an [n8n account](https://n8n.io) to automate workflows.
2. Create a workflow with the following nodes:
   - **Webhook**: Captures Slack events and verifies Slack's challenge.
   - **Set Node**: Extracts `user_query` and `channel_id` from messages.
   - **Cleanup Node**: Removes mentions (e.g., `@slackAgentApp`) from queries.
   - **HTTP Server Node**: Forwards queries to the FastAPI `/query` endpoint via ngrok.
   - **Merge Node**: Combines query data and backend response into a JSON.
   - **Slack Node**: Sends the response back to the Slack workspace (requires authentication with your workspace).
3. Run the workflow and test by sending a query (e.g., `@slackAgentApp how to install dependencies`) in Slack.

### Streamlit UI Setup (Alternative)

For users preferring a web interface over Slack:
1. Create an n8n workflow with:
   - **Webhook**: Passes queries from Streamlit to the FastAPI backend.
   - **HTTP Server Node**: Uses ngrok to expose the local server.
   - **Respond to Webhook**: Formats and returns responses to Streamlit.
2. Run the Streamlit app:
   ```bash
   streamlit run chatbot_frontend.py
   ```

## Usage

- **Slack**: Mention the bot in a channel or DM (e.g., `@slackAgentApp how to install dependencies`).
- **Streamlit**: Access the web UI, enter a query, and view the response.

## Example

**Slack Query**:
```
@slackAgentApp How do I install dependencies?
```
**Response**:
```
Run `pip install -r requirements.txt` in your virtual environment.
```

## Technical Details

- **Document Indexing** (`app.py`):
  - Loads documents from `documentation/` using `SimpleDirectoryReader`.
  - Generates OpenAI embeddings with `VectorStoreIndex`.
  - Stores embeddings in ChromaDB under `storage/developer_documents_collection`.
- **Query Handling** (`main.py`):
  - FastAPI backend with `/query` endpoint for processing questions.
  - Uses precomputed index from `storage/` for efficient responses.

## Contributing

Contributions are welcome! Open an issue or submit a pull request to enhance **slackAgent**.