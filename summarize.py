# Summarize text passages and extract keywords

from summa.keywords import keywords
from summa.summarizer import summarize
import re

def register(_bot):
    global bot
    bot = _bot
    bot.register_trigger('!keywords', extract_keywords)
    bot.register_trigger('!summarize', summarize_text)

def sanitize(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

async def extract_keywords(client, message):
    text = sanitize(message.content)
    words = keywords(text, split=True)
    bot.debug('Extracting keywords of text: {}. Keywords: {}'.format(text, str(words)))
    await client.send_message(message.channel, 'Keywords:\n' + '\n'.join(words))

async def summarize_text(client, message):
    command = sanitize(message.content)
    words = command.split(' ')
    try:
        if len(words) >= 3:
            ratio = float(words[1])
            if ratio <= 0 or ratio >= 1:
                raise ValueError('ratio must be between 0 and 1! (exclusive)')
            text = ' '.join(words[2:])
            summary = summarize(text, ratio=ratio)
            await client.send_message(message.channel, 'Summary:\n' + summary)
        else:
            raise ValueError('Invalid command format! Format must be !summarize [ratio] [text]')
    except Exception as e:
        await client.send_message(message.channel, str(e))
