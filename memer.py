# Respond when people get mentioned

import json
import random

def register(_bot):
    global bot
    bot = _bot
    global users
    bot.debug(users)
    for user_id in users:
        username, discriminator = user_id.split('#')
        bot.register_mention_subscriber(username, discriminator, get_message)
    
with open('resources/memes.info') as file:
    global users
    users = file.read().strip()
    users = json.loads(users)

global last_id
last_id = None
    
async def get_message(client, message):
    global last_id
    bot.debug('Last id: {}'.format(last_id))
    if last_id != message.id:
        last_id = message.id
        mentions = message.mentions
        for user in mentions:
            user_id = '{}#{}'.format(user.name, user.discriminator)
            global users
            if user_id in users:
                await client.send_message(message.channel, random.choice(users[user_id]))