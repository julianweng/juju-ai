#!/bin/bash
source ./passcode.txt

# rasa run --enable-api --cors "*"
rasa run actions &

# simple chatroom
python -m http.server 80 -d ./public & 

# discord bot
python bots/discordbot.py &

rasa x &