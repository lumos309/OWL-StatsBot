URL = "https://api.overwatchleague.com/stats/players?stage_id=regular_season"

PLAYER_RESPONSE = (
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

COMPARISON_RESPONSE = (
    "# {} vs. {}\n\n"
    "{}: {} for {}.  \n{}: {} for {}.\n\n---\n\n"
    "| Statistics                         | {}     | {}     |\n"
    "|:-----------------------------------|:-------|:-------|\n"
    "| Average eliminations per 10min     | {:.2f} | {:.2f} |\n"
    "| Average deaths per 10min           | {:.2f} | {:.2f} |\n"
    "| Average hero damage per 10min      | {:.2f} | {:.2f} |\n"
    "| Average healing per 10min          | {:.2f} | {:.2f} |\n"
    "| Average ultimates earned per 10min | {:.2f} | {:.2f} |\n"
    "| Average final blows per 10min      | {:.2f} | {:.2f} |\n"
    "| Total Time Played (hours)          | {:.2f} | {:.2f} |"
)

FOOTER = (
    "\n\nAll stats sourced from [here]({link}).\n\n"
    "---\n"
    "^(I am a bot and this action was performed automatically)  \n"
    "^(Send me a PM to provide feedback)"
).format(link=URL)

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
    'VAL': 'Los Angeles Valiant',
    'FLA': 'Florida Mayhem',
    'SEO': 'Seoul Dynasty'
}

PLAYERS = {
    'sbb': 'Saebyeolbe',
    'sdb': 'ShaDowBurn',
    'zebbo': 'Zebbosai',
    'rjh': 'ryujehong'
}