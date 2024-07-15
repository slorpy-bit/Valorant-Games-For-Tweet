from time import sleep
from datetime import datetime

while True:
    now = datetime.now()
    if now == now.replace(hour=22):
        print('Tiempo [SI]')
    else:
        print(now)
    sleep(40 * 60)
