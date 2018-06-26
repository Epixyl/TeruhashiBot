import discord
from riotwatcher import RiotWatcher
from requests import HTTPError
import datetime
import random
from Pymoe import Kitsu
from time import sleep

#Own files
import strings
import constants
import secrets
from helpers import *

#Caches
users = {}
leagues = {}
updated = {}
matchlists = {}
matches = {}
updatedmatch = {}
rankedmatchlist = {}
updatedrankedmatchlist = {}
updatedmatchlist = {}

async def handle_stalk(client, message, command, sudo, watcher):
    now_date = datetime.datetime.now()
    now = int(float(now_date.timestamp())) * 1000
    if(1 != len(command['args'])):
        await form_message(client, message, strings.PARAM_MSG)
        return

    if(is_dirty(command['args'][0])):
        await form_message(client, message, strings.DIRTY_ARG_MSG)
        return

    name = command['args'][0]
    #Fetch data if not in cache.
    if(name not in updated or (now_date - updated[name] > datetime.timedelta(minutes=constants.CACHE_REFRESH))):
        print('[CMD] --- Updating stats cache')
        users[name] = watcher.summoner.by_name(constants.LEAGUE_REGION, name)
        leagues[name] = watcher.league.positions_by_summoner(constants.LEAGUE_REGION, users[name]['id'])
        updated[name] = now_date

    # Get Ranked soloq stats.
    detected = False
    for league in leagues[name]:
        if(league['queueType'] == 'RANKED_SOLO_5x5'):
            detected = True
            await form_message(client, message, "%s is %s %s %dLP. (%dW/%dL)" % (name, league['tier'], league['rank'], league['leaguePoints'], league['wins'], league['losses']))
    
    if(detected == False):
        await form_message(client, message, "%s is unranked." % (name))
    else:
        #Also get ranked history
        if(name not in updatedrankedmatchlist or now_date - updatedrankedmatchlist[name] > datetime.timedelta(minutes=constants.CACHE_REFRESH)):
            print('[CMD] --- Updating rankedmatchlist cache')
            rankedmatchlist[name] = watcher.match.matchlist_by_account(constants.LEAGUE_REGION, users[name]['accountId'], queue=420, begin_index=0, end_index=10)
            print(rankedmatchlist[name])
            updatedrankedmatchlist[name] = now_date

        wins = 0
        played = len(rankedmatchlist[name]['matches'])
        for matchstub in rankedmatchlist[name]['matches']:

            if(matchstub['gameId'] not in updatedmatch or now_date - updatedmatch[matchstub['gameId']] > datetime.timedelta(minutes=constants.CACHE_REFRESH)):
                print('[CMD] --- Updating match cache')
                matches[matchstub['gameId']] = watcher.match.by_id(constants.LEAGUE_REGION, matchstub['gameId'])
                updatedmatch[matchstub['gameId']]= now_date

            #Find player
            participantId = 0
            for player in matches[matchstub['gameId']]['participantIdentities']:
                if(player['player']['accountId'] == users[name]['accountId']):
                    participantId = player['participantId']
                    break
            
            #Find who won
            winner = -1
            for team in matches[matchstub['gameId']]['teams']:
                if(team['win'] == 'Win' and matches[matchstub['gameId']]['gameDuration'] > 300):
                    winner = team['teamId']
                    break

            for participant in matches[matchstub['gameId']]['participants']:
                if(participant['participantId'] == participantId):
                    if(participant['teamId'] == winner):
                        wins = wins + 1

        await form_message(client, message, "winning %d of the last %d ranked games played." % (wins, played))

    # Get Matchlist
    if(name not in updatedmatchlist  or now_date - updatedmatchlist[name]> datetime.timedelta(minutes=constants.CACHE_REFRESH)):
        print('[CMD] --- Updating matchlist cache')
        matchlists[name] = watcher.match.matchlist_by_account(constants.LEAGUE_REGION, users[name]['accountId'], begin_index=0, end_index=10)
        updatedmatchlist[name] = now_date
        #print (matchlists[name])

    
    print("Current time is ", now)
    for matchstub in matchlists[name]['matches']:

        #If most recent match is too old, no need to check anything.
        if(now - int(matchstub['timestamp']) > constants.WIN_OF_THE_DAY_DELAY):
            await form_message(client, message, "First win of the day is available!")
            return

        if(matchstub['gameId'] not in updatedmatch or now_date - updatedmatch[matchstub['gameId']] > datetime.timedelta(minutes=constants.CACHE_REFRESH)):
            print('[CMD] --- Updating match cache')
            matches[matchstub['gameId']] = watcher.match.by_id(constants.LEAGUE_REGION, matchstub['gameId'])
            updatedmatch[matchstub['gameId']]= datetime.datetime.now()

        #Find player
        participantId = 0
        for player in matches[matchstub['gameId']]['participantIdentities']:
            if(player['player']['accountId'] == users[name]['accountId']):
                participantId = player['participantId']
                break
        
        #Find who won
        winner = -1
        for team in matches[matchstub['gameId']]['teams']:
            if(team['win'] == 'Win' and matches[matchstub['gameId']]['gameDuration'] > 300):
                winner = team['teamId']
                break

        for participant in matches[matchstub['gameId']]['participants']:
            if(participant['participantId'] == participantId):
                if(participant['teamId'] == winner):
                    #await form_message(client, message, "Game at %d result: WIN" % match['gameId']['gameCreation'])
                    if(now - int(matches[matchstub['gameId']]['gameDuration']) * 1000 - matches[matchstub['gameId']]['gameCreation'] <= constants.WIN_OF_THE_DAY_DELAY):
                        await form_message(client, message, "First win of the day is NOT available!")
                        return

    await form_message(client, message, "First win of the day might be available! (Need to check more matches!)")
    return