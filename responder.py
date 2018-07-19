import requests
import os
import re
import praw
from constants import URL, PLAYER_RESPONSE, COMPARISON_RESPONSE, FOOTER, TEAMS, PLAYERS

STATS = requests.get(URL).json()['data']
STAGE_STATS = ['', '', '', ''] # only load these if needed

SUBREDDIT = 'competitiveoverwatch'
PLAYER_COMMAND = re.compile('!stats (.*)', re.IGNORECASE)
STAGE_COMMAND = re.compile('stage[1-4]', re.IGNORECASE)

def player_stats(p, stage):
    reply = None
    player_name = PLAYERS.get(p.lower(), p).lower()
    if stage == 0: # show stats for all stages
        for player in STATS:
            if player['name'].lower() == player_name:
                reply = PLAYER_RESPONSE.format(
                    player['name'],
                    player['role'].title(),
                    TEAMS.get(player['team'], player['team']),
                    player['eliminations_avg_per_10m'],
                    player['deaths_avg_per_10m'],
                    player['hero_damage_avg_per_10m'],
                    player['healing_avg_per_10m'],
                    player['ultimates_earned_avg_per_10m'],
                    player['final_blows_avg_per_10m'],
                    player['time_played_total'] / 60 / 60
                ) + FOOTER
                break
    else:
        for player in STAGE_STATS[stage - 1]:
            if player['name'].lower() == player_name:
                reply = PLAYER_RESPONSE.format(
                    player['name'] + ' in Stage ' + str(stage),
                    player['role'].title(),
                    TEAMS.get(player['team'], player['team']),
                    player['eliminations_avg_per_10m'],
                    player['deaths_avg_per_10m'],
                    player['hero_damage_avg_per_10m'],
                    player['healing_avg_per_10m'],
                    player['ultimates_earned_avg_per_10m'],
                    player['final_blows_avg_per_10m'],
                    player['time_played_total'] / 60 / 60
                ) + FOOTER
                break

    return reply

def player_comparison(p1, p2, stage):
    reply = None
    player1, player2 = None, None
    player1_name = PLAYERS.get(p1.lower(), p1).lower()
    player2_name = PLAYERS.get(p2.lower(), p2).lower()
    if stage == 0:
        for player in STATS:
            if player['name'].lower() == player1_name:
                player1_name = player['name']
                player1 = player
            if player['name'].lower() == player2_name:
                player2_name = player['name']
                player2 = player
    else:
        for player in STAGE_STATS[stage - 1]:
            if player['name'].lower() == player1_name:
                player1_name = player['name']
                player1 = player
            if player['name'].lower() == player2_name:
                player2_name = player['name']
                player2 = player
    if player1 is not None and player2 is not None:
        reply = COMPARISON_RESPONSE.format(
            player1_name, player2_name + ' in Stage ' + str(stage),
            player1_name, player1['role'].title(), TEAMS.get(player1['team'], player1['team']),
            player2_name, player2['role'].title(), TEAMS.get(player2['team'], player2['team']),
            player1_name, player2_name,
            player1['eliminations_avg_per_10m'], player2['eliminations_avg_per_10m'],
            player1['deaths_avg_per_10m'], player2['deaths_avg_per_10m'],
            player1['hero_damage_avg_per_10m'], player2['hero_damage_avg_per_10m'],
            player1['healing_avg_per_10m'], player2['healing_avg_per_10m'],
            player1['ultimates_earned_avg_per_10m'], player2['ultimates_earned_avg_per_10m'],
            player1['final_blows_avg_per_10m'], player2['final_blows_avg_per_10m'],
            player1['time_played_total'] / 60 / 60, player2['time_played_total'] / 60 / 60
        ) + FOOTER
    return reply

def login():
    print('logging in ...')
    client = praw.Reddit(
        username      = os.environ.get('REDDIT_USER'),
        password      = os.environ.get('REDDIT_PASS'),
        client_id     = os.environ.get('CLIENT_ID'),
        client_secret = os.environ.get('CLIENT_SECRET'),
        user_agent    = 'OWL-StatsBot responder'
    )
    return client

def run(client):
    print('running ...')
    for comment in client.subreddit(SUBREDDIT).comments(limit=None):
        if comment.saved or comment.author == client.user.me():
            continue

        bot_call = PLAYER_COMMAND.search(comment.body)
        if bot_call is None:
            continue

        print('found comment: https://reddit.com' + comment.permalink)
        print('command:', bot_call.group(0))
        terms = bot_call.group(1).strip().split(' ')
        # check if stage is specified
        stage = 0
        for term in terms:
            selected_stage = STAGE_COMMAND.search(term)
            if selected_stage != None:
                stage = int(selected_stage.group(0)[-1])
                terms.remove(term)
        # retrieve stats for stage if not already loaded
        if STAGE_STATS[stage - 1] == '':
            STAGE_URL = URL[:-14] + 'stage' + str(stage)
            STAGE_STATS[stage - 1] = requests.get(STAGE_URL).json()['data']
    
        reply = player_stats(terms[0], stage) if len(terms) == 1 else player_comparison(terms[0], terms[1], stage)

        if reply is not None:
            comment.reply(reply)
            comment.save()
            print('replied')
        else:
            print('failed')


client = login()
run(client)

print('COMPLETE')
