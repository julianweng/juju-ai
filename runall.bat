start "" rasa run --enable-api --cors "*"
start "" rasa run actions
start "" python bots\discordbot.py
start "" http-server -p 80
rem === run ngrok to expose your app on the internet
rem start "" ngrok http 80