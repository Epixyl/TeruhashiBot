#Strings
PARAM_MSG = '{0.author.mention}, your command does not have the right number of params! (Try !help)'
NAN_MSG = 'That\'s not a valid number, {0.author.mention}.'
INVALID_COMMAND_MSG = 'I didn\'t understand that, {0.author.mention}. (Try !help)'
SHOULDI_YES_MSG = 'That sounds like a great idea, {0.author.mention}!'
SHOULDI_NO_MSG = 'I don\'t think that\'s such a good idea, {0.author.mention}.'
SHOULDI_REPEAT_YES_MSG = '{0.author.mention}, I already told you that it\'s a great idea!'
SHOULDI_REPEAT_NO_MSG = '{0.author.mention}, I already told you that I don\'t think that\'s such a good idea.'
DIRTY_ARG_MSG = 'Umm... I don\'t think that\'s a valid argument, {0.author.mention}.'
QUOTE_ERROR_MSG = '{0.author.mention}, I didn\'t know how to interpret your quotation marks!'
DISCONNECT_MSG = 'Bye!'
ROLL_MSG = 'Congratulations {0.author.mention}, you rolled a %d out of %d!'
SEARCH_SUCCESS_MSG = '{0.author.mention}, here\'s what I found:\n%s'
SEARCH_FAILURE_MSG = '{0.author.mention}, I couldn\'t find anything that matched your search!'
CHOOSE_MSG = '{0.author.mention}, of those choices, I pick %s!'
CHOOSE_REPEAT_MSG = '{0.author.mention}, I already told you that I choose %s!'
ADMIN_ACTION_SUCCESS_MSG = 'Success'
ADMIN_ACTION_FAILURE_MSG = 'Failure'
NO_PERMISSIONS_MSG = '{0.author.mention}, you do not have the permissions to do that!'
DUPLICATE_COMMAND_MSG = '{0.author.mention}, that command is already in use!'
GREETING_MSG = 'Hi, {0.author.mention}!'
FAREWELL_MSG = 'Bye, {0.author.mention}!'
SAIKI_MSG = ':flushed:'
PM_MSG = '{0.author.mention}, I PM\'d you the information you requested.'
ADD_CUSTOM_COMMAND_MSG = '{0.author.mention}, I added your command: %s -> %s.\n(Note: commands may be removed or replaced by other users without notice.)'
LIST_CUSTOM_COMMAND_MSG = '{0.author.mention}, Here are all the valid commands for your current channel: \n%s'
MESSAGE_DEBUG = '[CMD %s] SRVR=%s, USER=%s: '
REPLY_DEBUG = '[CMD %s] %s: '
TO_CHANNEL_DEBUG = '[CMD %s] SRVR=%s: '
BLOCKED_DEBUG = '[CMD %s] Command blocked due to blacklist'
ANIME_RESULT_MSG = '**Title:** %s\n**Link:** %s\n**Rating Percentile:** %s\n**Length:** %s hrs\n**Airing Dates:** %s to %s\n'
MANGA_RESULT_MSG = '**Title:** %s\n**Link:** %s\n**Rating Rank:** %s (%s%%)\n**Popularity Rank:** %s\n**Volumes:** %s\n**Release Dates:** %s to %s\n**Synopsis:** %s'
WHOIS_RESULT_MSG = '**Name:** %s\n**Description:** %s\n'
TOENGLISH_RESULT_MSG = '**Detected Language:** %s\n**Pronounciation:** %s\n**Translation:** %s\n'
DELTA_FORMAT = '%i days, %i hours, %i minutes, and %i seconds'
HELP_MSG = """
Here's some commands you can use:
**!examplecmd [Req. Arg] (Opt. Arg):** Description
**!anime [query]:** Find details about an anime.
**!manga [query]:** Find details about a manga.
**!whois [query]:** Find details about a character in an anime or manga.
**!translate [query]:** Translate some text to English.
**!roll (number):** Draw lots.
**!should [i, we, he, she, etc...action?]:** Make a yes/no decision.
**!is [query]:** Make a yes/no decision.
**!choose [opt1] [opt2] (...)** Make a choice.
**!add [command] [reply]** Create a custom command (Limited to the current channel).
**!list** List the custom commands.
"""
ADMIN_HELP_MSG = """
Since you're an administrator for the channel, here's more commands you can use!
**!unblacklist:**　Let me respond on the current channel.
**!blacklist:** Prevent me from responding on the current channel.

I need 'Manage Messages' permissions to enable clean commands (I'll remove any unnecessary chat clutter when using commands).
I need 'Manage Emojis' permissions to enable emoji management commands.
You can grant these permissions by creating a 'Bot' role in your server settings.
"""

ABOUT_MSG = """
I've been online for %s.

I'm written in Python 3 and maintained by @Epi#8979.
Version 1.1
"""
