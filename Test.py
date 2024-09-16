from requests_oauthlib import OAuth1Session
from time import sleep
from datetime import datetime
from os import system
from platform import platform
from random import choice
from get_files import get_file
import requests
import get_games_from_file
import get_online_games
import keys


consumer_key, consumer_secret = keys.main()

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

while True:
    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
        break
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )
    except requests.exceptions.ConnectionError:
        print('Error de conexion\nEsperando internet\n')
    sleep(100)

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Clean screen
system('cls' if 'windows' in platform().lower() else 'clear')

# Making the request
target = {'hour': 11, 'minute': 0, 'second': 0, 'microsecond': 0}
emotes = "⌚🥵🤩🪐🍫🎬🤟🤯👏🔥🚀💣🎇🔫☣️☕🌭☀️"
first_pass = False

now_target = datetime.now().replace(microsecond=0)

while True:
    # Check time
    now = datetime.now().replace(microsecond=0)
    print(f'Esperando reinicio... {(now_target - now).total_seconds()} segundos!\n')
    sleep((now_target - now).total_seconds())
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
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json={'text': tweet},
        )
        if response.status_code != 201:
            raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
        else:
            print("Response code: ", response.status_code)
            print("Tweet hecho con exito")
    else:
        print('No hay juegos hoy :(')
    now_target = now.replace(day=now.day + 1, hour=target['hour'], minute=target['minute'], second=target['second'],
                             microsecond=target['microsecond'])
