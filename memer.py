# Respond when people get mentioned

import json
import random

def register(_bot):
    global bot
    bot = _bot
    for user_id in users:
        username, discriminator = user_id.split('#')
        bot.register_mention_subscriber(username, discriminator, get_message)
    
with open('resources/memes.info') as file:
    global users
    users = file.read().strip()
    users = json.loads(users)
    
last_id = None
    
async def get_message(client, message):
    global last_id
    if not last_id or last_id != message.id:
        last_id = message.id
        mentions = message.mentions
        for user in mentions:
            user_id = '{}#{}'.format(user.name, user.discriminator)
            if user_id in users:
                await client.send_message(message.channel, random.choice(users[user_id]))