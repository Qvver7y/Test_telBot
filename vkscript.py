import sys
#from tkinter import W
from datetime import time, datetime
import time as t

class vk_objective:
    def __init__(self, id, Time, delta, token ):  # delta - time between 2 verifacations
        self.id = id
        Time = Time.split(':')
        self.Time = time(int(Time[0]),int(Time[1]) )       
        self.delta = delta
        self.token = token

def get_curTime():
    timehelp = datetime.now()
    Curtime = time(timehelp.hour, timehelp.minute)
    return Curtime



def wait(Time):
    Curtime = get_curTime()         # using time class. time format: H:M
    while(Curtime < Time):
        t.sleep(30)
        Curtime = get_curTime()    
    #print(Curtime < Time)


def main(argv):
    f = open("tokenvk", 'r')
    tokenvk = f.readline()[0:-1]
    f.close()
    VKo = vk_objective(argv[1], argv[2], argv[3], tokenvk)
    wait(VKo.Time)    






if __name__ == "__main__":
    main(sys.argv)