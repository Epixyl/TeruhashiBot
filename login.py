import discord
from riotwatcher import RiotWatcher
from requests import HTTPError
import datetime
import random
from Pymoe import Kitsu
from time import sleep

#Own files
import secrets
import command as user
import admin
import strings
from helpers import *
import league
import weeb

#Credentials
DISCORD_TOKEN = secrets.DISCORD_TOKEN
RIOT_TOKEN = secrets.RIOT_TOKEN
ANIME_ID = secrets.ANIME_ID
ANIME_SECRET = secrets.ANIME_SECRET
OSU_TOKEN = secrets.OSU_TOKEN

#Objects
client = discord.Client()
anime_list = Kitsu(ANIME_ID, ANIME_SECRET)
watcher = RiotWatcher(RIOT_TOKEN)
blacklist = []

# Called whenever a message is posted into a Discord channel.
@client.event
async def on_message(message):

    #Update NOW constants
    now_date = datetime.datetime.now()

    #Ignore private messages.
    if message.channel.is_private:
        return

    #Check if the sender has admin authority.
    sudo = message.channel.server.owner.id == message.author.id


    command = parse_args(message.content)

    #Ignore statements that are not commands.
    if(not command['iscommand']):
        return

    if(command['isinvalid']):
        await form_message(client, message, strings.QUOTE_ERROR_MSG)
        return

    if message.author == client.user:
        return

    ### ADMINISTRATIVE COMMANDS: Can be used in any channel regardless of blacklist.
    if command['command'].lower() == 'blacklist':
        await admin.handle_blacklist(client, message, command, sudo, blacklist)
        return

    if command['command'].lower() == 'unblacklist':
        await admin.handle_unblacklist(client, message, command, sudo, blacklist)
        return
 
    #Enforce blacklist
    if(message.channel.id in blacklist):
        debug(strings.BLOCKED_DEBUG, "")
        return

    debug(strings.MESSAGE_DEBUG % (str(now_date), message.channel.id, message.author.id), message.content)

    # Hidden Ofu! feature.
    if 'ofu' in message.content.lower():
        await form_private_message(client, message, ':innocent:')
        #NO RETURN

    # Pings the bot to see if it's online.
    if command['command'].lower() in ['hello', 'hi', 'greet', 'ping']:
        await user.handle_hello(client, message, command, sudo)
        return

    if command['command'].lower() in ['bye', 'goodbye', 'ban']:
        await user.handle_bye(client, message, command, sudo)
        return 

    # Roll a number between 0 and a number.
    if command['command'].lower() in ['roll', 'r']:
        await user.handle_roll(client, message, command, sudo)
        return

    # Choose an option from many.
    if command['command'].lower() in ['choose', 'select', 'pick', 'choosefrom', 'c']:
        await user.handle_choose(client, message, command, sudo)
        return

    # Pings the bot to see if it's online.
    if command['command'].lower() in ['should', 'shouldi', 'shouldwe']:
        await user.handle_should(client, message, command, sudo)
        return

    # See basic LoL stats on a specified User.
    if command['command'].lower() in ['stalk', 'see']:
        await league.handle_stalk(client, message, command, sudo, watcher)
        return

    # Find info on a anime
    if command['command'].lower() in ['info', 'anime', 'a']:
        await weeb.handle_anime(client, message, command, sudo, anime_list)
        return

    # Find info on a manga
    if command['command'].lower() in ['manga', 'm']:
        await weeb.handle_manga(client, message, command, sudo, anime_list)
        return

    if command['command'].lower() in ['help', 'h']:
        await user.handle_help(client, message, command, sudo)
        return

    if command['command'].lower() == 'ofu':
        return

    await form_message(client, message, strings.INVALID_COMMAND_MSG)
    return

@client.event
async def on_ready():
    debug('[SERVER] Logged in!', '')

#Load blacklist
debug('[SERVER] Loading blacklist', '')
try:
    wl = open('blacklist.txt', 'r')
    lines = wl.readlines()
    for line in lines:
        blacklist.append(line.strip('\n'))
    wl.close()
except FileNotFoundError:
    debug('[SERVER] No blacklist found', '')

debug('[SERVER] Logging on...', '')
client.run(DISCORD_TOKEN)