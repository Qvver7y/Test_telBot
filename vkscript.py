from os import access
from re import L
import sys
#from tkinter import W
from datetime import time, datetime
import time as t
import requests

class vk_objective:
    def __init__(self, id, Time, delta, token ):  # delta - time between 2 verifacations
        self.id = id
        Time = Time.split(':')
        self.Time = time(int(Time[0]),int(Time[1]) )       
        self.delta = int(delta)
        self.token = token
    def checkOnline(self):

        data = {"user_ids" :str(self.id), "fields" : "online"}
        res = self.send_req("users.get", data) 
        if(res["response"][0]["online"] == 0):
            return "N"  # Not online
        elif(res["response"][0]["online"] == 1):
            try:
                if(res["response"][0]["online_mobile"] == 1):
                    return "M" # Mobile
                else:
                    return "C" # Computer
            except:
                return "C" # Computer
        else:
            return "E" # error
    def send_req(self, method_name, data = None):
        data["access_token"] = self.token
        data["v"] = 5.131
       # data = {"PARAM" : data1, "access_token" : self.token, "v" : 5.131}
        return requests.post(f"https://api.vk.com/method/{method_name}",data=data).json()


def get_curTime():
    timehelp = datetime.now()
    Curtime = time(timehelp.hour, timehelp.minute)
    return Curtime

def work(vko):
    curTime = get_curTime()
    while(curTime < vko.Time):
        print(vko.checkOnline())
        t.sleep(vko.delta)
        curTime = get_curTime()
        
'''
def wait(Time):
    Curtime = get_curTime()         # using time class. time format: H:M
    while(Curtime < Time):
        t.sleep(30)
        Curtime = get_curTime()    
'''

def main(argv):
    f = open("tokenvk", 'r')
    tokenvk = f.readline()[0:-1]
    f.close()
    VKo = vk_objective(argv[1], argv[2], argv[3], tokenvk)
    #print(VKo.checkOnline())
    work(VKo)
#    data = {"user_ids" : "id254887735", "fields" : "online"}
#    print(VKo.send_req("users.get", data))
   # wait(VKo.Time)    






if __name__ == "__main__":
    main(sys.argv)