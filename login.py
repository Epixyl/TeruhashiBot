import discord
from riotwatcher import RiotWatcher
from requests import HTTPError
import datetime
import random
from Pymoe import Kitsu
from Pymoe import Anilist
from time import sleep
from googletrans import Translator

#Own files
import secrets
import command as user
import admin
import strings
import constants
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
character_list = Anilist()
watcher = RiotWatcher(RIOT_TOKEN)
translator = Translator()
blacklist = []
command_list = {}
starttime = 0

# Called whenever a message is posted into a Discord channel.
@client.event
async def on_message(message):

    #Update NOW constants
    now_date = datetime.datetime.now()

    #Check if the sender has admin authority.
    sudo = message.channel.is_private or message.channel.server.owner.id == message.author.id

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

    if command['command'].lower() == 'say':
        await admin.handle_say(client, message, command, sudo)
        return

    #Ignore private messages.
    if message.channel.is_private:
        return
 
    #Enforce blacklist
    if(message.channel.id in blacklist):
        debug(strings.BLOCKED_DEBUG, "")
        return

    debug(strings.MESSAGE_DEBUG % (str(now_date), message.channel.id, message.author.id), message.content)

    # Hidden Ofu! feature.
    if 'ofu' in message.content.lower():
        await client.add_reaction(message, constants.EMOJI_INNOCENT)
        #NO RETURN

    # Hidden Saiki feature.
    if 'saiki' in message.content.lower():
        await client.add_reaction(message, constants.EMOJI_BLUSHING)
        #NO RETURN

    # Hidden Teruhashi feature.
    if 'teruhashi' in message.content.lower():
        await client.add_reaction(message, constants.EMOJI_BLUSHING)
        #NO RETURN

    # Hidden tooru feature.
    if 'makoto' in message.content.lower():
        await client.add_reaction(message, constnats.EMOJI_ANGRY)
        #NO RETURN

    # Hidden aiura feature.
    if 'aiura' in message.content.lower():
        await client.add_reaction(message, constnats.EMOJI_ANGRY)
        #NO RETURN

    if command['command'].lower() in ['uptime', 'owner', 'about', 'ping']:
        await admin.handle_about(client, message, command, sudo, starttime)
        return

    # Pings the bot to see if it's online.
    if command['command'].lower() in ['hello', 'hi', 'greet']:
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

    # Magic 8 ball.
    if command['command'].lower() in ['is', 'are', 'yesno']:
        await user.handle_is(client, message, command, sudo)
        return

    # See basic LoL stats on a specified User.
    if command['command'].lower() in ['stalk', 'see']:
        await league.handle_stalk(client, message, command, sudo, watcher)
        return

    # Translate stuff to english.
    if command['command'].lower() in ['translate', 'english', 't', 'eng', 'trans']:
        await weeb.handle_toenglish(client, message, command, sudo, translator)
        return

    # Find info on a anime
    if command['command'].lower() in ['info', 'anime', 'a']:
        await weeb.handle_anime(client, message, command, sudo, anime_list)
        return

    # Find info on a character
    if command['command'].lower() in ['character', 'char', 'whois', 'w']:
        await weeb.handle_whois(client, message, command, sudo, character_list)
        return

    # Find info on a manga
    if command['command'].lower() in ['manga', 'm']:
        await weeb.handle_manga(client, message, command, sudo, anime_list)
        return

    if command['command'].lower() in ['help', 'h']:
        await user.handle_help(client, message, command, sudo)
        return

    if command['command'].lower() in ['code']:
        await user.handle_code(client, message, command, sudo)
        return

    if command['command'].lower() in ['add']:
        await user.handle_custom_add(client, message, command, sudo, command_list)
        return

    if (message.channel.id, command['command'].lower()) in command_list:
        await user.handle_custom(client, message, command, sudo, command_list)
        return

    await form_message(client, message, strings.INVALID_COMMAND_MSG)
    return

@client.event
async def on_ready():
    debug('[SERVER] Logged in!', '')

#Load blacklist
debug('[SERVER] Loading blacklist', '')
try:
    wl = open(constants.BLACKLIST_FILE, 'r')
    lines = wl.readlines()
    for line in lines:
        blacklist.append(line.strip('\n'))
    wl.close()
except FileNotFoundError:
    debug('[SERVER] No blacklist found', '')

#Load custom commands
debug('[SERVER] Loading custom commands', '')
try:
    wl = open(constants.COMMAND_LIST_FILE, 'r')
    lines = wl.readlines()
    for line in lines:
        server_name = line.split(':')[0]
        custom_command = line.split(':')[1]
        custom_reply = ' '.join(line.split(':')[2:])
        command_list[(server_name, custom_command)] = custom_reply
    wl.close()
except FileNotFoundError:
    debug('[SERVER] No custom commands found', '')

debug('[SERVER] Logging on...', '')
starttime = datetime.datetime.now()
client.run(DISCORD_TOKEN)