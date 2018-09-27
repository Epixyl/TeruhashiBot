import discord
import datetime
import random

#Own files
import strings
import constants
import secrets

def parse_args(message):
    args = {}
    quote = False
    temp = []

    #Handle quotations
    parts = message.replace('“','"').replace('”','"').split('"')
    for part in parts:
        if(quote):
            temp.append(part)
        else:
            temp.extend(part.split(' '))
        quote = not quote

    args['command'] = temp[0][1:]
    args['args'] = list(filter(lambda x: len(x) > 0, temp[1:]))
    args['isinvalid'] = not quote
    args['iscommand'] = temp[0].startswith('!') and not is_dirty(temp[0][1:])
    return args

def is_dirty(arg):
    for char in constants.CHAR_BLACKLIST:
        if (char in arg):
            return True
    return False

def is_integer(arg):
    for char in arg:
        if(char not in constants.NUMBERS):
            return False
    try:
        int(arg)
        return True
    except ValueError:
        return False

def to_link(title):
    words = title.lower().split(' ')
    name = '-'.join(words)
    return name

async def form_message(client, message, text):
    now_date = datetime.datetime.now()
    msg = text.format(message)
    await client.send_message(message.channel, msg)
    debug(strings.REPLY_DEBUG % (str(now_date), 'PUBLIC REPLY'), msg)
    return

async def form_message_to_channel(client, message, channelid, text):
    now_date = datetime.datetime.now()
    msg = text.format(message)
    await client.send_message(client.get_channel(channelid), msg)
    debug(strings.TO_CHANNEL_DEBUG % (str(now_date), channelid), msg)
    return

async def form_private_message(client, message, text):
    now_date = datetime.datetime.now()
    msg = text.format(message)
    await client.send_message(message.author, msg)
    debug(strings.REPLY_DEBUG % (str(now_date), 'PRIVATE REPLY'), msg)
    return

async def delete_message(client, message):
    now_date = datetime.datetime.now()
    content = message.content
    try:
        await client.delete_message(message)
        debug(strings.REPLY_DEBUG % (str(now_date), 'DELETE MESSAGE'), content)
        return True
    except:
        debug(strings.REPLY_DEBUG % (str(now_date), 'FAILED TO DELETE MESSAGE'), content)
    return False

async def form_reaction(client, message, reaction_unicode):
    now_date = datetime.datetime.now()
    await client.add_reaction(message, reaction_unicode)
    debug(strings.REPLY_DEBUG % (str(now_date), 'ADDED REACTION'), repr(reaction_unicode))
    return

def debug(header, msg):
    print(header + msg + '\n')
    if(constants.DEBUG):
        wl = open('debug.log', 'ab')
        wl.write((header + msg + '\n').encode('utf8'))
        wl.close()