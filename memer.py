# Respond when people get mentioned

import json
import random
import time

last_id = None # Prevent replying to duplicate messages

config_cooldown_trigger = '!cooldown'
last_mention = {}
mention_cooldown = 5 # Won't meme again if mentioned multiple times within timespan
    
with open('resources/memes.info') as file:
    users = file.read().strip()
    users = json.loads(users)

with open('resources/gif_memes.info') as file:
    gif_info = json.loads(file.read().strip())

def register(_bot):
    global bot
    bot = _bot
    global users

    for trigger in gif_info:
        bot.register_trigger(trigger, create_gif_sender(gif_info[trigger]))

    bot.register_trigger(config_cooldown_trigger, config_cooldown)
    bot.debug(users)
    for user_id in users:
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
        for user in mentions:
            user_id = '{}#{}'.format(user.name, user.discriminator)
            global users
            if user_id in users:
                curr_time = time.time()
                if user_id in last_mention:
                    if curr_time - last_mention[user_id] <= mention_cooldown:
                        continue
                last_mention[user_id] = curr_time
                await client.send_message(message.channel, random.choice(users[user_id]))

async def config_cooldown(client, message):
    user = '{}#{}'.format(message.author.name, message.author.discriminator)
    if user in bot.admins:
        global mention_cooldown
        mention_cooldown = float(message.content.split(' ')[-1])
        await client.send_message(
                message.channel,
                'Mention cooldown reconfigured to: {:.2f} seconds'.format(mention_cooldown))