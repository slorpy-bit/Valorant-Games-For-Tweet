from datetime import datetime
from time import sleep


def tweet_4teams(team1, team2, team3, team4, vct_server, hour1, hour2):
    draw_tweet = f"""\
Partidos de hoy de la #{vct_server}:

Horas CDMX:
- {hour1} | {team1} vs {team2}
- {hour2} | {team3} vs {team4}\
"""
    return draw_tweet


games = [
    {'title': {'text': tweet_4teams('KRU', 'G2', 'TH', 'LEV', 'VCTAmericas', 2, 3)},
     'time': datetime(2024, 7, 13, 2, 14, 30)}
]

print(datetime.now())

while len(games) > 0:
    for game in games:
        if game['time'] <= datetime.now():
            print(game['title']['text'])
            """
            response = oauth.post(
                "https://api.twitter.com/2/tweets",
                json=game['title'],
            )
            """
            games.remove(game)
            break
        sleep(5)
