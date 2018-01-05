# React with isaac emojis
def register(_bot):
    global bot
    bot = _bot
    bot.register_message_subscriber(get_message)
    
with open('resources/reactions.info') as file:
    global emojis
    emojis = file.readlines()
    emojis = [x.strip() for x in emojis]

with open('resources/server.info') as file:
    global server_id
    server_id = file.read()

async def get_message(client, message):
    if 'isaac' in message.content.lower():
        bot.debug('Isaac detected in message. Reacting with emojis.')
        for emoji_name in emojis:
            emoji_id = emoji_name.replace('>','').split(':')[-1]
            emoji = get_emoji(client, emoji_id)
            if emoji == None:
                bot.debug('Tried to find isaac emoji, but emoji not found!')
            await client.add_reaction(message, emoji)
            bot.debug('Succesfully reacted with emoji={}'.format(emoji_id))

def get_emoji(client, emoji_id):
    for emoji in client.get_server(server_id).emojis:
        if emoji.id == emoji_id:
            return emoji
    return None