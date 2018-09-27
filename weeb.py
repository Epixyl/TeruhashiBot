import discord
import datetime
import random
from Pymoe import Kitsu
from Pymoe import Anilist

#Own files
import strings
import constants
import secrets
from helpers import *

worstanime = 0

async def handle_anime(client, message, command, sudo, anime_list):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return

    result = anime_list.anime.search(' '.join(command['args']))

    if(result == None):
        await form_message(client, message, strings.SEARCH_FAILURE_MSG)
        return

    try:
        canonicalTitle = result[0]['attributes']['canonicalTitle']
        animeid = result[0]['id']
        link = constants.ANIME_LINK_HEADER + to_link(animeid)
        image = result[0]['attributes']['posterImage']['tiny']
        ratingRank = result[0]['attributes']['ratingRank']
        lowestRank = worstanime
        if(worstanime == 0):
            lowestRank = anime_list.anime.search('tenkuu danbzai skelter heaven')[0]['attributes']['ratingRank']
        ratingPercentile = 'Not rated yet!'
        if(ratingRank is not None and lowestRank is not None):
            ratingPercentile = 'Top {:.2f}%'.format((float(ratingRank) * 100.0 / float(lowestRank)))
        print(ratingRank, lowestRank, ratingPercentile)
        synopsis = result[0]['attributes']['synopsis']
        episodeCount = result[0]['attributes']['episodeCount']
        episodeLength = result[0]['attributes']['episodeLength']
        if episodeLength is None or episodeLength == 0:
            length = 'Estimated ' + '{:.1f}'.format((episodeCount * 24) / 60.0)
        else:
            length = '{:.1f}'.format((episodeCount * episodeLength) / 60.0)
        startDate = result[0]['attributes']['startDate']
        endDate = result[0]['attributes']['endDate']
        if result[0]['attributes']['endDate'] is None:
            endDate = '??? (Still Airing)'
        output = strings.ANIME_RESULT_MSG % (canonicalTitle, link, ratingPercentile, length, startDate, endDate)

        await form_message(client, message, strings.SEARCH_SUCCESS_MSG % output)
    except:
        await form_message(client, message, strings.SEARCH_FAILURE_MSG)
    return

async def handle_manga(client, message, command, sudo, anime_list):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return

    result = anime_list.manga.search(' '.join(command['args']))

    if(result == None):
        await form_message(client, message, strings.SEARCH_FAILURE_MSG)
        return

    canonicalTitle = result[0]['attributes']['canonicalTitle']
    mangaid = result[0]['id']
    link = constants.MANGA_LINK_HEADER + to_link(mangaid)
    output = strings.MANGA_RESULT_MSG % (canonicalTitle, link, result[0]['attributes']['ratingRank'], result[0]['attributes']['averageRating'] if result[0]['attributes']['averageRating'] != None else 'n/a', result[0]['attributes']['popularityRank'], result[0]['attributes']['volumeCount'] if result[0]['attributes']['volumeCount'] != 0 else 'Unknown', result[0]['attributes']['startDate'], result[0]['attributes']['endDate'] if result[0]['attributes']['endDate'] != None else '??? (Still Ongoing)', result[0]['attributes']['synopsis'])

    await form_message(client, message, strings.SEARCH_SUCCESS_MSG % output)
    return

async def handle_whois(client, message, command, sudo, character_list):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return

    char_info = character_list.search.character(' '.join(command['args']),1,1) #page 1, show only one result.

    

    try:
        result = character_list.get.character(char_info['data']['Page']['characters'][0]['id'])
    except:
        await form_message(client, message, strings.SEARCH_FAILURE_MSG)
        return

    print (result)
    output = strings.WHOIS_RESULT_MSG % (result['data']['Character']['name']['first'] + ' ' + result['data']['Character']['name']['last'] + ((' (' + result['data']['Character']['name']['native'] + ')') if result['data']['Character']['name']['native'] != None else ''), result['data']['Character']['description'][:1500].replace('<br>', '\n') + ('...' if len(result['data']['Character']['description']) > 1500 else ''))

    await form_message(client, message, strings.SEARCH_SUCCESS_MSG % output)
    return

async def handle_toenglish(client, message, command, sudo, translator):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return

    try:
        query = ' '.join(command['args'])
        result = translator.translate(query)
        pronounciation = translator.translate(query, result.src)
    except:
        await form_message(client, message, strings.SEARCH_FAILURE_MSG)
        return

    print (result)
    output = strings.TOENGLISH_RESULT_MSG % (result.src, pronounciation.pronunciation, result.text)

    await form_message(client, message, (strings.SEARCH_SUCCESS_MSG % output)[:1800] + ('...' if len(output) > 1800 else ''))
    return