from requests_oauthlib import OAuth1Session
from time import sleep
from datetime import datetime


def tweet_4teams(team1, team2, team3, team4, vct_server, hour1, hour2):
    draw_tweet = f"""\
Partidos de hoy de la #{vct_server}:

Horas CDMX:
- {hour1} | {team1} vs {team2}
- {hour2} | {team3} vs {team4}\
"""
    return draw_tweet


hashtags = {'americas': '#VCTAmericas', 'emea': '#VCTEmea', 'pacifico': '#VCTPacific', 'china': '#VCTChina'}

games = [
    {'title': {'text': tweet_4teams('KRU', 'G2', 'TH', 'LEV', hashtags['americas'], '2pm', '3pm')},
     'time': datetime(2024, 7, 13, 2, 38)}
]

consumer_key = "tn48s2ybVVXcf3k8ISUzzVB4y"
consumer_secret = "fRvSZatoVdqXKyGskdhdez0FhtDZCgMzjUw07iiABssqlFfk1r"

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

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

# Making the request
while len(games) > 0:
    for game in games:
        if game['time'] <= datetime.now():
            response = oauth.post(
                "https://api.twitter.com/2/tweets",
                json=game['title'],
            )
            games.remove(game)

            if response.status_code != 201:
                raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
            else:
                print("Response code: ", response.status_code)
                print("Tweet hecho con exito")

            break
    sleep(5)
