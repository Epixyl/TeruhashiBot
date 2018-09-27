import discord
import datetime
import random
from threading import Lock

#Own files
import strings
import constants
import secrets
from helpers import *

# Caches
shouldis = {}
updatedshouldi = {}
choices = {}
updatedchoices = {}
command_lock = Lock()

async def handle_saiki(client, message, command, sudo):
    if(0 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    await form_message(client, message, strings.SAIKI_MSG)
    return

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
    await form_private_message(client, message, strings.HELP_MSG)
    if(sudo):
        await form_private_message(client, message, strings.ADMIN_HELP_MSG)
    permissions = await delete_message(client, message)
    if not permissions:
        await form_message(client, message, strings.HELP_MSG)
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
    now_date = datetime.datetime.now()
    already = True
    query = ' '.join(sorted(command['args'])).lower()
    if(query not in choices or (now_date - updatedchoices[query] > datetime.timedelta(minutes=constants.SHOULDI_CACHE_REFRESH))):
        choices[query] = command['args'][random.randint(0,len(command['args'])-1)]
        updatedchoices[query] = now_date
        already = False

    if(already):
        await form_message(client, message, strings.CHOOSE_REPEAT_MSG % choices[query])
    else:
        await form_message(client, message, strings.CHOOSE_MSG % choices[query])
    return

async def handle_should(client, message, command, sudo):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return
    now_date = datetime.datetime.now()
    query = 'should' + message.author.name.lower() + ' '.join(command['args']).lower()
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
        await form_reaction(client, message, constants.EMOJI_THUMBS_UP)
        await form_message(client, message, strings.SHOULDI_YES_MSG)
    else:
        await form_reaction(client, message, constants.EMOJI_THUMBS_DOWN)
        await form_message(client, message, strings.SHOULDI_NO_MSG)
    return

async def handle_is(client, message, command, sudo):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return
    now_date = datetime.datetime.now()
    query = 'is' + message.author.name.lower() + ' '.join(command['args']).lower()
    already = True
    if(query not in shouldis or (now_date - updatedshouldi[query] > datetime.timedelta(minutes=constants.IS_CACHE_REFRESH))):
        shouldis[query] = random.randint(0,1)
        updatedshouldi[query] = now_date
        already = False

    if(shouldis[query] == 1 and already):
        await form_reaction(client, message, constants.EMOJI_THUMBS_UP)
    elif(shouldis[query] == 0 and already):
        await form_reaction(client, message, constants.EMOJI_THUMBS_DOWN)
    elif(shouldis[query] == 1):
        await form_reaction(client, message, constants.EMOJI_THUMBS_UP)
    else:
        await form_reaction(client, message, constants.EMOJI_THUMBS_DOWN)
    return

async def handle_custom(client, message, command, sudo, command_list):
    if(len(command['args']) != 0):
        await form_message(client, message, strings.PARAM_MSG)
        return

    custom_command = (message.channel.id, command['command'].lower())
    print(command_list[custom_command])
    if custom_command in command_list:
        await form_message(client, message, command_list[custom_command])
        return

    await form_message(client, message, strings.INVALID_COMMAND_MSG)
    return

async def handle_custom_add(client, message, command, sudo, command_list):
    if(len(command['args']) < 2):
        await form_message(client, message, strings.PARAM_MSG)
        return

    custom_command = command['args'][0].lower()
    custom_reply = ' '.join(command['args'][1:])

    if is_dirty(custom_command):
        await form_message(client, message, strings.DIRTY_ARG_MSG)
        return

    command_lock.acquire()
    if custom_command in constants.OFFICIAL_COMMANDS:
        await form_message(client, message, strings.DUPLICATE_COMMAND_MSG)
        return

    command_list[(message.channel.id, custom_command)] = custom_reply
    wr = open(constants.COMMAND_LIST_FILE, 'r')
    lines = wr.readlines()
    wr.close()
    wl = open(constants.COMMAND_LIST_FILE, 'w')
    for line in lines:
        if (message.channel.id + ':' + custom_command) in line:
            wl.write(message.channel.id + ':' + custom_command + ':' + custom_reply + '\n')
        else:
            wl.write(line)
    wl.close()
    command_lock.release()

    await form_private_message(client, message, strings.ADD_CUSTOM_COMMAND_MSG % (custom_command, custom_reply))

    permissions = await delete_message(client, message)
    if not permissions:
        await form_message(client, message, strings.ADD_CUSTOM_COMMAND_MSG % (custom_command, custom_reply))

    return