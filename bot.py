# Main Bot module

# Import libraries
import discord
import asyncio
from datetime import datetime
import sys
from os.path import exists
from os import makedirs

# Redirect stderr to error log
if not exists('error_logs'):
    makedirs('error_logs')
sys.stderr = open('error_logs/{}.log'.format(datetime.now().strftime('%m-%d-%y_%I-%M')), 'w') 

# Create client object
client = discord.Client()

class Bot(object):
    admins = []
    _triggers = {} # key=first word : value=list of funcs to call
    _user_subscribers = {} # key=username#discriminator : value=list of funcs to call
    _mention_subscribers = {} # key=username#discriminator : value=list of funcs to call
    _message_subscribers = set() # funcs to call
    _pause_triggers = set()
    _resume_triggers = set()
    _activity_rotation = [] # list of str of activities
    activity_timer = 60 * 20 # seconds to wait until switching activities
    paused = False
    
    def pause(self):
        self.paused = True
    def resume(self):
        self.paused = False
    
    def start_activity_rotation(self):
        """
        Starts activity rotation, changing activity every `activity_timer` seconds
        """
        async def rotation():
            index = 0
            while not client.is_closed and len(self._activity_rotation) > 0:
                await self.change_activity(self._activity_rotation[index])
                await asyncio.sleep(self.activity_timer)
                index = (index + 1) % len(self._activity_rotation)
        # Set loop in background
        if len(self._activity_rotation) > 0:
            client.loop.create_task(rotation())
            bot.debug('Started activity rotation!')
        else:
            bot.debug('Tried to start activity rotation but there are no activities in rotation!')
            
        
    async def change_activity(self, activity):
        """
        Change activity text for bot
        
        Parameters
        --------------
        activity : str
            str to display as activity
        """
        bot.debug('Changed activity to {}'.format(activity))
        await client.change_presence(game=discord.Game(name=activity))
    
    def add_activities(self, *activities):
       """
       Add activities to activity rotation
       
       Parameters
       --------------
       *activities : tuple of str
           these str will be appended to the end of the rotation
       """
       self._activity_rotation.extend(activities)
       bot.debug('Added activities to activity rotation for activies={}'.format(str(activities)))
       
    def register_flow_triggers(self, pause, resume):
        """
        Pauses bot when pause is first word of function.
        Resumes bot when resume is first word of function.
        
        Parameters
        ------------
        pause : str
            bot will be paused when this is the first word of any message
        resume : str
            bot will be resumed when this is the first word of any message
        """
        self._pause_triggers.add(pause)
        self._resume_triggers.add(resume)
    
    def register_trigger(self, trigger, func):
        """
        Registers func to be called when trigger is the first word of a message
        
        Parameters
        ------------
        trigger : str
            func will be called when this is the first word of any message
        func : method
            func will be called with params `client`, `message`, where `client` is a discord.Client object, and `message` is a discord.Message object
        """
        if trigger in self._triggers:
            self._triggers[trigger].append(func)
        else:
            self._triggers[trigger] = [func]
        bot.debug('Added trigger subscriber for trigger={}'.format(trigger))
        
    def register_mention_subscriber(self, name, discriminator, func):
        """
        Registers func to be called when specified user is mentioned
        
        Parameters
        --------------
        name : str
            username of user. Name in `name#discriminator`.
        discriminator : str
            discriminator of user. Discriminator in `name#discriminator`.
        func : method
            func will be called with params `client`, `message`, where `client` is a discord.Client object, and `message` is a discord.Message object
        """
        key = '{}#{}'.format(name, discriminator)
        if key in self._mention_subscribers:
            self._mention_subscribers[key].append(func)
        else:
            self._mention_subscribers[key] = [func]
        bot.debug('Added mention subscriber for user={}#{}'.format(name, discriminator))
        
    def register_user_subscriber(self, name, discriminator, func):
        """
        Registers func to be called when user sends any message
        
        Parameters
        --------------
        name : str
            username of user. Name in `name#discriminator`.
        discriminator : str
            discriminator of user. Discriminator in `name#discriminator`.
        func : method
            func will be called with params `client`, `message`, where `client` is a discord.Client object, and `message` is a discord.Message object
        """
        key = '{}#{}'.format(name, discriminator)
        if key in self._user_subscribers:
            self._user_subscribers[key].append(func)
        else:
            self._user_subscribers[key] = [func]
        bot.debug('Added user subscriber for user={}#{}'.format(name, discriminator))
            
            
    def register_message_subscriber(self, func):
        """
        Registers func to be called when any message is sent
        
        Parameters
        -------------
        func : method
            func will be called with params `client`, `message`, where `client` is a discord.Client object, and `message` is a discord.Message object
        """
        self._message_subscribers.add(func)
        bot.debug('Added message subscriber')
    
    def debug(self, debug_log, add_timestamp = True):
        date = str(datetime.now().replace(microsecond=0))
        message = debug_log
        if(add_timestamp):
            message = '{} : {}'.format(date, debug_log)        
        print(message)
        with open('debug.log', 'a') as log:
            log.write('{}\n'.format(message))
    
def import_all():
    import os
    from os.path import isfile, dirname, abspath
    exceptions = {__file__.split('/')[-1], '__init__.py', 'rnn.py', 'josh_memer.py', 'ian_memer.py'}
    for module in os.listdir(dirname(abspath(__file__))):
        if not isfile(module) or module[-3:] != '.py' or module in exceptions:
            continue
        module = module[:-3]
        bot.debug('Importing and registering module: {}'.format(module))
        imported = __import__(module, locals(), globals())
        if not hasattr(imported, 'register'):
            bot.debug('Module {} doesn\'t implement register(bot) method!'.format(module))
            continue
        imported.register(bot)
        bot.debug('Done importing and registering module: {}'.format(module))
    del os, module, isfile, dirname, abspath
    

@client.event
async def on_ready():
    bot.debug('', add_timestamp = False)
    bot.debug('Logged in as {} : {}'.format(client.user.name, client.user.id))
    bot.debug('---------------------------------------', add_timestamp = False)
    import_all()
    bot.add_activities('with himself', 'hard to get', 'with fire', 'in the superbowl', 'hooky')
    bot.start_activity_rotation()
    bot.debug('Ready!')
    for server in client.servers:
        try:
            await client.send_message(server.default_channel, 'Hello, world!')
            bot.debug('Sent awake message to default channel of channel: {}'.format(server.name))
        except:
            bot.debug('Error sending message to default channel of a server!')
    
@client.event
async def on_message(message):
    await flow_control_triggers(message)
    if not bot.paused:
        await call_trigger_subscribers(message)
        await call_mention_subscribers(message)
        await call_user_subscribers(message)
        await call_message_subscribers(message)
        
async def flow_control_triggers(message):
    user = '{}#{}'.format(message.author.name, message.author.discriminator)
    if user not in bot.admins:
        return None
    trigger = message.content.strip().split(' ')[0]
    if trigger in bot._resume_triggers:
        bot.debug('id={} : Resume called by admin {}'.format(message.id, user))
        await client.send_message(message.channel, 'I\'m baaaaaaack!')
        bot.resume()
    elif trigger in bot._pause_triggers:
        bot.debug('id={} : Pause called by admin {}'.format(message.id, user))
        await client.send_message(message.channel, 'I\'m going to sleep now.')
        bot.pause()
    
async def call_user_subscribers(message):
    key = '{}#{}'.format(message.author.name, message.author.discriminator)
    if key in bot._user_subscribers:
        for func in bot._user_subscribers[key]:
            await func(client, message)
        num_subscribers = len(bot._user_subscribers[key])
        bot.debug('id={} : Called {} user subscriber(s) for user {}'.format(message.id, num_subscribers, key))
        
async def call_mention_subscribers(message):
    for user in message.mentions:
        key = '{}#{}'.format(user.name, user.discriminator)
        if key in bot._mention_subscribers:
            for func in bot._mention_subscribers[key]:
                await func(client, message)
            num_subscribers = len(bot._mention_subscribers[key])
            bot.debug('id={} : Called {} mention subscriber(s) for user {}'.format(message.id, num_subscribers, key))
        

async def call_message_subscribers(message):
    if len(bot._message_subscribers) > 0:
        for sub in bot._message_subscribers:
            await sub(client, message)
        bot.debug('id={} : Called {} message subscriber(s)!'.format(message.id, len(bot._message_subscribers)))

async def call_trigger_subscribers(message):
    trigger = message.content.strip().split(' ')[0]
    if trigger in bot._triggers:
        for func in bot._triggers[trigger]:
            await func(client, message)
        num_subscribers = len(bot._triggers[trigger])
        bot.debug('id={} : Called {} trigger subscriber(s) for trigger {}'.format(
                message.id, num_subscribers, trigger))
        
bot = Bot()
info = {}
with open('resources/auth.info') as file:
    lines = file.readlines()
    for line in lines:
        parts = line.split(' ')
        info[parts[0]] = parts[1]

finished = False
while not finished:
    try:
        client.run(info['token'])
        finished = True
    except ConnectionResetError:
        bot.debug('Encountered ConnectionResetError! Rebooting now.')
    except:
        bot.debug('The client crashed! Rebooting now.')
sys.exit(0)