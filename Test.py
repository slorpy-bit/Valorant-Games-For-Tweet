from time import sleep
from datetime import datetime
from os import system
from platform import platform
from random import choice
from get_files import get_file
from get_twitter_api import get_api_main
import get_games_from_file
import get_online_games


def main():
    # Clean screen
    system('cls' if 'windows' in platform().lower() else 'clear')

    # Making the request
    target = {'hour': 11, 'minute': 0, 'second': 0, 'microsecond': 0}
    emotes = "⌚🥵🤩🪐🍫🎬🤟🤯👏🔥🚀💣🎇🔫☣️☕🌭☀️"
    while True:
        # Check time
        now = datetime.now().replace(day=datetime.now().day+1)
        # Get from files
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
        if len(games_today) > 1:
            tweet = '\n'.join(games_today)
            print('\n' + tweet + '\n')
        else:
            print('No hay juegos hoy :(')
        sleep(100)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nAdios!')
