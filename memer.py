# Respond when people get mentioned

import json
import random
import time

last_id = None # Prevent replying to duplicate messages

config_cooldown_trigger = '!cooldown'
last_mention = {}
mention_cooldown = 5 # Won't meme again if mentioned multiple times within timespan

def load_meme_info():
    """Load the file from disk containing the user id and memes
    
    Returns
    -------
    dict
        Dict describing the users and their memes. Keys are strings with the discord id of the user. (username#tag)
        Values are a list of strings, which are the memes to be sent out.
    """
    with open('resources/memes.info') as file:
        users = file.read().strip()
        users = json.loads(users)
    return users

def load_gif_info():
    """Load the file from disk containing the gif information.
    
    Returns
    -------
    dict
        Keys are strings with the discord id of the user. (username#tag)
        Values are a string, signifying the path to the gif to be sent.
    """

    with open('resources/gif_memes.info') as file:
        gif_info = json.loads(file.read().strip())
    return gif_info

def register(_bot):
    global bot
    bot = _bot

    meme_info = load_meme_info()
    gif_info = load_gif_info()

    for trigger in gif_info:
        bot.register_trigger(trigger, create_gif_sender(gif_info[trigger]))

    bot.register_trigger(config_cooldown_trigger, config_cooldown)
    bot.debug(meme_info)
    for user_id in meme_info:
        username, discriminator = user_id.split('#')
        bot.register_mention_subscriber(username, discriminator, get_message)

def create_gif_sender(path):
    async def sender(client, message):
        bot.debug('Sending gif: {}'.format(path))
        await client.send_file(message.channel, path)
    return sender
    
async def get_message(client, message):
    global last_id
    bot.debug('Last id: {}'.format(last_id))
    if last_id != message.id:
        last_id = message.id
        mentions = message.mentions
        meme_info = load_meme_info()
        for user in mentions:
            user_id = '{}#{}'.format(user.name, user.discriminator)
            if user_id in meme_info.keys():
                curr_time = time.time()
                if user_id in last_mention:
                    if curr_time - last_mention[user_id] <= mention_cooldown:
                        continue
                last_mention[user_id] = curr_time
                await client.send_message(message.channel, random.choice(meme_info[user_id]))

async def config_cooldown(client, message):
    user = '{}#{}'.format(message.author.name, message.author.discriminator)
    if user in bot.admins:
        global mention_cooldown
        mention_cooldown = float(message.content.split(' ')[-1])
        await client.send_message(
                message.channel,
                'Mention cooldown reconfigured to: {:.2f} seconds'.format(mention_cooldown))