from random import randint
from time import sleep

old = lastest = 0

for i in range(100):
    switch = randint(0,1)
    if switch:
        pass
    else:
        lastest+=1
    lastest = i
    if lastest != old:
        print("changed")
        old = lastest
    elif lastest == old:
        print("same")
    print("lastest value:",lastest,"old value:",old)
    sleep(1)
        