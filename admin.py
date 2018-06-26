import discord
import datetime

#Own files
import secrets
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
        wl = open('blacklist.txt', 'a')
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
        wr = open('blacklist.txt', 'r')
        lines = wr.readlines()
        wr.close()
        wl = open('blacklist.txt', 'w')
        for line in lines:
            if not message.channel.id in line:
                wl.write(line)
        wl.close()
    else:
        await form_message(client, message, strings.ADMIN_ACTION_FAILURE_MSG)
        return

    await form_message(client, message, strings.ADMIN_ACTION_SUCCESS_MSG)
    return