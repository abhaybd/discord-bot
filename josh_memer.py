# Respond when josh gets messaged

def register(_bot):
    global bot
    bot = _bot
    username, discriminator = user_id.split('#')
    bot.register_mention_subscriber(username, discriminator, get_message)
    
with open('resources/josh.info') as file:
    global user_id
    user_id = file.read()
    
async def get_message(client, message):
    await client.send_message(message.channel, 'haha what a faggot')