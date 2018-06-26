#Strings
PARAM_MSG = 'Your command does not have the right number of params! (Try !help)'
NAN_MSG = 'That\'s not a valid number, {0.author.mention}.'
INVALID_COMMAND_MSG = 'I didn\'t understand that, {0.author.mention}. (Try !help)'
SHOULDI_YES_MSG = 'That sounds like a great idea, {0.author.mention}!'
SHOULDI_NO_MSG = 'I don\'t think that\'s such a good idea, {0.author.mention}.'
SHOULDI_REPEAT_YES_MSG = '{0.author.mention}, I already told you that it\'s a great idea!'
SHOULDI_REPEAT_NO_MSG = '{0.author.mention}, I already told you that I don\'t think that\'s such a good idea.'
DIRTY_ARG_MSG = 'Umm... I don\'t think that\'s a valid argument, {0.author.mention}.'
QUOTE_ERROR_MSG = 'I didn\'t know how to interpret your quotation marks!'
DISCONNECT_MSG = 'Bye!'
ROLL_MSG = 'Congratulations {0.author.mention}, you rolled a %d out of %d!'
SEARCH_SUCCESS_MSG = '{0.author.mention}, here\'s what I found:\n%s'
SEARCH_FAILURE_MSG = '{0.author.mention}, I couldn\'t find anything that matched your search!'
CHOOSE_MSG = '{0.author.mention}, of those choices, I choose %s!'
ADMIN_ACTION_SUCCESS_MSG = 'Success'
ADMIN_ACTION_FAILURE_MSG = 'Failure'
NO_PERMISSIONS_MSG = 'You do not have the permissions to do that!'
GREETING_MSG = 'Hi, {0.author.mention}!'
FAREWELL_MSG = 'Bye, {0.author.mention}!'
MESSAGE_DEBUG = '[CMD %s] SRVR=%s, USER=%s: '
REPLY_DEBUG = '[CMD %s] %s: '
BLOCKED_DEBUG = '[CMD %s] Command blocked due to blacklist'
ANIME_RESULT_MSG = '**Title:** %s\n**Link:** %s\n**Rating Rank:** %s (%s%%)\n**Popularity Rank:** %s\n**Episodes:** %s\n**Airing Dates:** %s to %s\n**Synopsis:** %s'
MANGA_RESULT_MSG = '**Title:** %s\n**Link:** %s\n**Rating Rank:** %s (%s%%)\n**Popularity Rank:** %s\n**Volumes:** %s\n**Release Dates:** %s to %s\n**Synopsis:** %s'
HELP_MSG = """
**!examplecmd [Req. Arg] (Opt. Arg):** Description
**!stalk [summonerName]:** Stalk a League of Legends summoner.
**!info [query]:** Find details about an anime. 
**!manga [query]:** Find details about a manga.
**!roll (number):** Draw lots.
**!should (i, we, he, she, etc...action?):** Make a yes/no decision.
**!choose [opt1] [opt2] (...)** Make a choice.
"""
ADMIN_HELP_MSG = """
Since you're an administrator for the channel, here's more commands you can use!
**!unblacklist:**　Let me respond on the current channel.
**!blacklist:** Prevent me from responding on the current channel.

(Note: I do not respond to private chat messages.)
"""