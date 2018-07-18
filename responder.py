import requests
import os
import re
import praw

URL = "https://api.overwatchleague.com/stats/players?stage_id=regular_season"
STATS = requests.get(URL).json()['data']

SUBREDDIT = 'competitiveoverwatch'
COMMAND = re.compile('!stats (.*)', re.IGNORECASE)

TEAMS = {
    'BOS': 'Boston Uprising',
    'GLA': 'Los Angeles Gladiators',
    'HOU': 'Houston Outlaws',
    'SFS': 'San Fransisco Shock',
    'LDN': 'London Spitfire',
    'SHD': 'Shanghai Dragons',
    'NYE': 'New York Excelsior',
    'PHI': 'Philadelphia Fusion',
    'DAL': 'Dallas Fuel',
    'VAL': 'Los Angeles Valient',
    'FLA': 'Florida Mayhem',
    'SEO': 'Seoul Dynasty'
}

PLAYERS = {
    'sbb': 'Saebyeolbe',
    'sdb': 'ShaDowBurn',
    'zebbo': 'Zebbosai',
    'rjh': 'ryujehong'
}

RESPONSE = (
    "# Statistics for {}\n\n"
    "Role: {}  \nTeam: {}\n\n---\n\n"
    "| Statistics | |\n|:--|:--|\n"
    "| Average eliminations per 10min     | {:.2f} |\n"
    "| Average deaths per 10min           | {:.2f} |\n"
    "| Average hero damage per 10min      | {:.2f} |\n"
    "| Average healing per 10min          | {:.2f} |\n"
    "| Average ultimates earned per 10min | {:.2f} |\n"
    "| Average final blows per 10min      | {:.2f} |\n"
    "| Total Time Played (hours)          | {:.2f} |"
)
FOOTER = (
    "\n\nAll stats sourced from [here]({link}).\n\n"
    "---\n"
    "^(I am a bot and this action was performed automatically)  \n"
    "^(Send me a PM to provide feedback)"
).format(link = URL)

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

        bot_call = COMMAND.search(comment.body)
        if bot_call is None:
            continue

        print('found comment: https://reddit.com' + comment.permalink)
        print('term:', bot_call.group(1))
        term = bot_call.group(1).strip()
        term = PLAYERS.get(term.lower(), term)
        reply = None

        for player in STATS:
            if player['name'].lower() == term.lower():
                reply = RESPONSE.format(
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
        
        if reply is not None:
            print(reply)
            comment.reply(reply)
            comment.save()
            print('replied')
        else:
            print('failed')


client = login()
run(client)

print('COMPLETE')