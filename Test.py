from requests_oauthlib import OAuth1Session
from time import sleep
from datetime import datetime
import requests
import get_games_from_file
import get_online_games
import keys

# Making the request
tournaments = ['VCT', 'VCL', 'Champions', 'VCT:', 'GC']
while True:
    games_today = ["Partidos de hoy"]
    checked_games = []
    now = datetime.now()
    if now.hour == 2:
        games = get_games_from_file.main()
        for game in games:
            if (((game['date'].day <= now.day and
                    any(tournament in game['server'].split(' ') for tournament in tournaments)) and
                    len(games_today) != 6) and game not in checked_games):
                games_today.append(f"{game['server']} | {game['left']} vs {game['right']}")
                checked_games.append(game)
        print('\n' + "\n".join(games_today) + '\n')
        tweet = '\n'.join(games_today)
        print('Esperando reinicio... \n')
    else:
        print('Aun no es la hora indicada... \n')
    sleep(35 * 60)
