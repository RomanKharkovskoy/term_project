from random import randint
from time import sleep
import os

if randint(1, 6) == 3:
    print("Пока, дружище))")
    for i in range(10, 0, -1):
        print(i)
        sleep(1)
    os.system('shutdown -r -t 0')
