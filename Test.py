from datetime import datetime
import get_games_from_file


def get_server():
    servers = ['VCT', 'VCL']

    games_today = ["Partidos de hoy"]
    now = datetime.now()
    # get_online_games.main()
    games = get_games_from_file.main()
    for game in games:
        if (game['date'] <= now.replace(day=now.day) and any(server in game['server'].split(' ') for server in servers) and
                len(games_today) != 6):
            games_today.append(f"{game['server']} | {game['left']} vs {game['right']}")
    print('\n' + "\n".join(games_today) + '\n')

    my_string = (
        "holdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwo"
        "adaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadah"
        "oldwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadaholdwoadah")
    print('Mi string:', len(my_string))
    print('Games:', len(''.join(games_today)))


if __name__ == '__main__':
    pass
