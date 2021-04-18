import requests
import json
import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        res = self.talk2rasa(message.content,message.author)
        await message.channel.send(res)

    def talk2rasa(self, req, user):
        #if req.startswith('$inspire'):
        #    return ""
        
        url = 'http://localhost:5005/webhooks/rest/webhook'
        q = {'message': req, 'sender': str(user)}
        x = requests.post(url, json = q)
        a = json.loads(x.text)
        for i in a:
            res = i['text']
            print(req, user, res)
            return(res)

client = MyClient()
client.run(os.getenv('DISCORD_PASS'))
