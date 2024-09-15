from requests_oauthlib import OAuth1Session
from time import sleep
from datetime import datetime
from os import system
from platform import platform
from random import choice
import get_games_from_file
import get_online_games


def get_file(path: str):
    with open(path, 'r') as f:
        return f.read().split('\n')


# Clean screen
system('cls' if 'windows' in platform().lower() else 'clear')

# Emotes
emotes = "⌚🥵🤩🪐🍫🎬🤟🤯👏🔥🚀💣🎇🔫☣☕🌭☀"

# Making the request
target = {'hour': 11, 'minute': 0, 'second': 0, 'microsecond': 0}
first_pass = False
while True:
    # Check time
    now = datetime.now()
    now_target = now.replace(day=now.day + 1,
                             hour=target['hour'],
                             minute=target['minute'],
                             second=target['second'],
                             microsecond=target['microsecond'])
    if not first_pass:
        print('No es la hora indicada... Esperando tiempo: '
              f'{(now_target - datetime.now().replace(microsecond=0)).total_seconds()}')
        first_pass = True
    frases = get_file('frases.txt')
    arrobas = get_file('arrobas.txt')
    tournaments = get_file('tournaments.txt')
    # Start function
    games_today = [f"{choice(frases)} {choice(['en', 'para'])} @{choice(arrobas)} {choice(emotes)}\n"]
    checked_games = []
    get_online_games.main()
    games = get_games_from_file.main()
    for game in games:
        if (((game['date'].day <= now.day and
                any(tournament in game['server'].split(' ') for tournament in tournaments)) and
                len(games_today) != 6) and game not in checked_games):
            games_today.append(f"{game['server']} | {game['left']} vs {game['right']}")
            checked_games.append(game)
    tweet = '\n'.join(games_today)
    if len(games_today) > 1:
        print('\n' + tweet + '\n')
    else:
        print('No hay juegos hoy :(')
    break
