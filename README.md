# slackAgent

WorkFlow
## PART 1

- SETUP PYTHON(3.10 using pip), FOLDER STRUCTURE(.env(OPENAI API KEY), requirements, documentation dir, storage dir) 
"python3.10 -m venv venvSlackAgent"
"source venvSlackAgent/bin/activate"
"pip install -r requirements.txt"

- app.py ---> load openai key, documents, convert documents to vector embeddings and store in storage directory.
"python3.10 app.py"

- main.py ---> basic backend to answer user questions based on our vector database.
"uvicorn main:app --reload"

## NEXT UP AUTOMATE WORKFLOWS USING n8n