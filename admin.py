import discord
import datetime

#Own files
import secrets
import constants
import strings
from helpers import *

async def handle_blacklist(client, message, command, sudo, blacklist):
    if(not sudo):
        return

    if(0 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    if(message.channel.id not in blacklist):
        blacklist.append(message.channel.id)
        wl = open(constants.BLACKLIST_FILE, 'a')
        wl.write(message.channel.id + '\n')
        wl.close()
    else:
        await form_message(client, message, strings.ADMIN_ACTION_FAILURE_MSG)
        return

    await form_message(client, message, strings.ADMIN_ACTION_SUCCESS_MSG)
    return

async def handle_unblacklist(client, message, command, sudo, blacklist):
    if(not sudo):
        return

    if(0 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    if(message.channel.id in blacklist):
        blacklist.remove(message.channel.id)
        wr = open(constants.BLACKLIST_FILE, 'r')
        lines = wr.readlines()
        wr.close()
        wl = open(constants.BLACKLIST_FILE, 'w')
        for line in lines:
            if not message.channel.id in line:
                wl.write(line)
        wl.close()
    else:
        await form_message(client, message, strings.ADMIN_ACTION_FAILURE_MSG)
        return

    await form_message(client, message, strings.ADMIN_ACTION_SUCCESS_MSG)
    return

async def handle_about(client, message, command, sudo, starttime):
    #if(not sudo):
    #    return

    if(0 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    delta = (datetime.datetime.now() - starttime).seconds
    day = (datetime.datetime.now() - starttime).days
    hour, rem = divmod(delta, 3600)
    minute, sec = divmod(rem, 60)
    datestring = strings.DELTA_FORMAT % (day, hour, minute, sec)

    await form_message(client, message, strings.ABOUT_MSG % datestring)
    return

async def handle_say(client, message, command, sudo):
    if(not sudo):
        return
    if(len(command['args']) < 2):
        await form_message(client, message, strings.PARAM_MSG)
        return
    channelid = command['args'][0]
    msg = ' '.join(command['args'][1:])
    try:
        await form_message_to_channel(client, message, channelid, msg)
    except:
        await form_message(client, message, strings.ADMIN_ACTION_FAILURE_MSG)
    await form_message(client, message, strings.ADMIN_ACTION_SUCCESS_MSG)
