# Respond when Ian gets messaged

import random

def register(_bot):
    global bot
    bot = _bot
    username, discriminator = user_id.split('#')
    bot.register_mention_subscriber(username, discriminator, get_message)
    
with open('resources/ian.info') as file:
    global user_id
    user_id = file.read()
    
roast_messages = ['g-g-g-g-gaaaaaaaaaay',
                  "Say that louder. I don't think he heard you from that deep in the closet.",
                  'What, you egg!']
    
async def get_message(client, message):
    await client.send_message(message.channel, random.choice(roast_messages))