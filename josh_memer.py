# Respons when josh gets messaged

def register(_bot):
    global bot
    bot = _bot
    bot.register_message_subscriber(get_message)
    
with open('josh.info') as file:
    global user_id
    user_id = file.read()
    
async def get_message(client, message):
    for user in message.mentions:
        username = '{}#{}'.format(user.name, user.discriminator)
        if user_id == username:
            await client.send_message(message.channel, 'haha what a faggot')