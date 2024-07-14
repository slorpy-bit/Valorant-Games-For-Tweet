import requests
import pickle
from re import findall
from bs4 import BeautifulSoup
from time import sleep

games = []
num_games = 25

url = 'https://liquipedia.net/valorant/Liquipedia:Matches'
response = requests.get(url).text
soup = BeautifulSoup(response, 'html.parser')
teams = {'left': soup.find_all(class_='team-template-team2-short'),
         'right': soup.find_all(class_='team-template-team-short')}
list_teams = {'left': str(teams['left']).split('><'), 'right': str(teams['right']).split('><')}
timers = soup.find_all(class_='timer-object timer-object-countdown-only')
n = 0
for left, right in zip(list_teams['left'], list_teams['right']):
    matches = {'left': findall(r'data-highlightingclass="([^"]+)"', left),
               'right': findall(r'data-highlightingclass="([^"]+)"', right)}
    timer = findall(r'>([^"]+) <', str(timers[n]))
    if matches['left'] and matches['right']:
        games.append({'team1': matches['left'][0], 'team2': matches['right'][0], 'date': timer[0]}.copy())
        n += 1
    if n == num_games:
        break
print(games)
print(len(games))
with open('games.pkl', 'wb') as f:
    pickle.dump(games, f)
