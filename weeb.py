import discord
import datetime
import random
from Pymoe import Kitsu

#Own files
import strings
import constants
import secrets
from helpers import *

async def handle_anime(client, message, command, sudo, anime_list):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return

    result = anime_list.anime.search(' '.join(command['args']))

    #print (result[0])
    if(result == None):
        await form_message(client, message, strings.SEARCH_FAILURE_MSG)

    output = strings.ANIME_RESULT_MSG % (result[0]['attributes']['canonicalTitle'], "(Under construction)", result[0]['attributes']['ratingRank'], result[0]['attributes']['averageRating'] if result[0]['attributes']['averageRating'] != None else 'n/a', result[0]['attributes']['popularityRank'], result[0]['attributes']['episodeCount'], result[0]['attributes']['startDate'], result[0]['attributes']['endDate'] if result[0]['attributes']['endDate'] != None else '??? (Still Airing)', result[0]['attributes']['synopsis'])

    await form_message(client, message, strings.SEARCH_SUCCESS_MSG % output)
    return

async def handle_manga(client, message, command, sudo, anime_list):
    if(len(command['args']) < 1):
        await form_message(client, message, strings.PARAM_MSG)
        return

    result = anime_list.manga.search(' '.join(command['args']))

    if(result == None):
        await form_message(client, message, strings.SEARCH_FAILURE_MSG)

    output = strings.MANGA_RESULT_MSG % (result[0]['attributes']['canonicalTitle'], "(Under construction)", result[0]['attributes']['ratingRank'], result[0]['attributes']['averageRating'] if result[0]['attributes']['averageRating'] != None else 'n/a', result[0]['attributes']['popularityRank'], result[0]['attributes']['volumeCount'] if result[0]['attributes']['volumeCount'] != 0 else 'Unknown', result[0]['attributes']['startDate'], result[0]['attributes']['endDate'] if result[0]['attributes']['endDate'] != None else '??? (Still Ongoing)', result[0]['attributes']['synopsis'])

    await form_message(client, message, strings.SEARCH_SUCCESS_MSG % output)
    return