# Talk like user

from os.path import isfile
             
with open('monitored.info') as file:
    global monitored
    monitored = file.readlines()

def register(bot_obj):
    global bot
    bot = bot_obj
    bot.register_trigger('!talklike', talk_like)
    for user in monitored:
        parts = user.split('#')
        name, discriminator = parts[0], parts[1]
        bot.register_user_subscriber(name, discriminator, get_message)
    
async def get_message(client, message):
    name = message.author.name
    file_name = '{}.csv'.format(name)
    print_header = not isfile(file_name)
    with open(file_name, 'a') as file:
        if print_header:
            file.write('date,epoch,message\n')
        date = str(message.timestamp.replace(microsecond=0))
        epoch = str(round(message.timestamp.timestamp()))
        file.write('{},{},{}\n'.format(date, epoch, message.content.replace('\n',' ')))      
    
async def talk_like(client, message):
    print('Not implemented!')