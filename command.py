import discord
import datetime
import random

#Own files
import strings
import constants
import secrets
from helpers import *

# Caches
shouldis = {}
updatedshouldi = {}

async def handle_hello(client, message, command, sudo):
    if(0 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    await form_message(client, message, strings.GREETING_MSG)
    return

async def handle_bye(client, message, command, sudo):
    if(0 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    await form_message(client, message, strings.FAREWELL_MSG)

async def handle_help(client, message, command, sudo):
    if(0 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    await form_message(client, message, strings.HELP_MSG)
    if(sudo):
        await form_private_message(client, message, strings.ADMIN_HELP_MSG)
    return

async def handle_roll(client, message, command, sudo):
    if(len(command['args']) > 1):
        await form_message(client, message, strings.PARAM_MSG)
        return

    top = constants.DEFAULT_ROLL
    if(len(command['args']) == 1):

        if(not is_integer(command['args'][0]) or int(command['args'][0]) <= 0):
            await form_message(client, message, strings.NAN_MSG)
            return

        top = int(command['args'][0])

    await form_message(client, message, strings.ROLL_MSG % (random.randint(0,top), top))
    return

async def handle_choose(client, message, command, sudo):
    if(len(command['args']) < 2):
        await form_message(client, message, strings.PARAM_MSG)
        return

    await form_message(client, message, strings.CHOOSE_MSG % command['args'][random.randint(0,len(command['args'])-1)])
    return

async def handle_should(client, message, command, sudo):
    now_date = datetime.datetime.now()
    query = message.author.name.lower() + ' '.join(command['args']).lower()
    already = True
    if(query not in shouldis or (now_date - updatedshouldi[query] > datetime.timedelta(minutes=constants.SHOULDI_CACHE_REFRESH))):
        shouldis[query] = random.randint(0,1)
        updatedshouldi[query] = now_date
        already = False

    if(shouldis[query] == 1 and already):
        await form_message(client, message, strings.SHOULDI_REPEAT_YES_MSG)
    elif(shouldis[query] == 0 and already):
        await form_message(client, message, strings.SHOULDI_REPEAT_NO_MSG)
    elif(shouldis[query] == 1):
        await form_message(client, message, strings.SHOULDI_YES_MSG)
    else:
        await form_message(client, message, strings.SHOULDI_NO_MSG)
    return