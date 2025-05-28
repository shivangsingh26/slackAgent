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


- setup n8n account(this is used for our workflow automation)

- Below are our nodes
- webhook - type of api connection that sends data from one application to another application on occurance of a specific event. 
- edit fields
- cleanup
- http server(ngrok)
- merge(edit fields+http server)
- slack api

- **ngrok** is used for running our local server using webhooks on n8n workflows
(Basically we will be able to run our local apis anywhere on the web)

- **slack api** used so that users can directly chat via slack, 

## What Is the Slack API?

- The Slack API lets you build bots and apps that can:

- Read messages from Slack
- Post messages
- Respond to user actions
- Automate workflows

## What Is the Events API?

- Slack's Events API lets your bot get notified when things happen in Slack — like when someone sends a message, joins a channel, reacts with an emoji, etc.

- You subscribe to events, and Slack sends you a payload (data) whenever that event occurs.

- create a new app in slack api, then setup bot token scopes

- 1.app_mentions:read ---> Allows your app to read messages where it is mentioned using @ (e.g., @slackAgent help)

- Use Case: You want your bot to react when someone calls it in a channel like @slackAgent how do I login?

- 2.chat:write ----------> Lets your bot post messages, replies, or updates in Slack conversations.

- Use Case: Respond to users, send alerts, welcome messages, etc.

- 3.channels:history ---->  Lets your bot read all messages in public channels where it's a member.

- Use Case: Useful if your bot needs to listen in on conversations or analyze past messages in channels like #general.

- turn on event subscriptions(and paste the n8n webhook url there)
when we send a post request a challenge parameter is created in the request body. this challenge parameter is sent back to slack api for verification.

- in order to capture the challenge parameter we need to set a challenge field in n8n. 

- also in webhook change respond field to **Using 'Respond to WebHook' Mode** .

- next go to enable events in slack api and paste the n8n url in request url field to trigger the workflow.(If your workflow is correct then it will show Verified.)

- next setup **subscribe to bot events**. Here we add 2 bot user events.

- message.channels - triggered when a message was posted to a channel

- message.im - triggered when a message was posted in a direct message(DM) channel


- next we get into our slack workspace we created, called slackAgent.(we will add our slackAgentApp created in slack api to our slack workspace.)

- **Bot Testing using n8n workflow**

- Firstly set Respond in webhook back to immediately as we set it just for testing slack api verification.

- Ask any query through slack channel.(eg - how to install dependencies)

- now we create a node which passes query, channel_id.

- we also create another node for cleanup of our query. because sometimes we might also get the mentions in our user_messsage and we need to remove them

- now using ngrok we will get this message to our local server. for this we create another node for http server(copy the ngrok url and paste it in that node)

- On executing the http request node we can see the output of our query.

- Next step is to get that output to our slackAgent workspace.

- For this firstly we use the Merge node(get data from set node(user_query, channel_id) and http server node's response) and combine them into a single json.

- Now we can use the slack node to send data to slackAgent Workspace.

- - It will ask for authentication and connection to your workspace. do that accordingly. 