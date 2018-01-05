commands = {'ping' : '!ping',
            'shutdown' : '!shutdown',
            'pause' : '!pause',
            'resume' : '!resume',
            'commands' : '!commands'}

def register(_bot):
    global bot
    bot = _bot
    bot.admins.extend(admins)
    bot.register_trigger(commands['ping'], ping)
    bot.register_trigger(commands['shutdown'], shutdown)
    bot.register_trigger(commands['commands'], get_commands)
    bot.register_flow_triggers(commands['pause'], commands['resume'])

with open('resources/admins.info') as file:
    global admins
    admins = file.readlines()
    admins = [x.strip() for x in admins]
          
async def ping(client, message):
    tag = get_tag(message)
    if tag in bot.admins:
        await client.send_message(message.channel, 'Pong!')

async def get_commands(client, message):
    await client.send_message(message.channel,
                              'I just DMed you a list of commands. You might not have permissions, though!')
    dm = '\n'.join(commands.values())
    await client.send_message(message.author, dm)
    
async def shutdown(client, message):
    tag = get_tag(message)
    if tag in bot.admins:
        bot.debug('Shutdown called by {}. Shutting down.'.format(tag))
        await client.send_message(message.channel, 'Bye bye!')
        import sys
        sys.stderr.close()
        await client.close()
        
def get_tag(message):
    tag = '{}#{}'.format(message.author.name, message.author.discriminator)
    return tag