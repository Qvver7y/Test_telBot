from os import access
import sys
import pandas as pd
from datetime import time, datetime, date
import time as t
import requests

class vk_objective:
    def __init__(self, id, Time, delta, token ):  # delta - time between 2 verifacations
        self.dict_ex = {}
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
    def WriteToExcel(self, dict_time, dict_status,file_name, dte):
        try:
            xl = pd.read_excel(file_name, sheet_name=0)
        except:
            dict = {dte:dict_time, f"Status{dte}": dict_status}
            xl = pd.DataFrame(data=dict)
            xl.to_excel(file_name)
        xl = xl.to_dict()
        if(dte in xl.keys):
            max_num = int(xl[dte].keys[-1]) + 1
            for i in range(0,len(dict)):
                xl[dte][i + max_num] = dict_time[i]
                xl[f"Status{dte}"][i + max_num] = dict_status[i]            
        else:
            xl[dte] = dict_time
            xl[f"Status{dte}"] = dict_status
        xl = pd.DataFrame(data = xl)
        xl.to_excel(file_name, index=0)

            
    def send_req(self, method_name, data = None):
        data["access_token"] = self.token
        data["v"] = 5.131
       # data = {"PARAM" : data1, "access_token" : self.token, "v" : 5.131}
        return requests.post(f"https://api.vk.com/method/{method_name}",data=data).json()
    def waitDelt(self):
        t.sleep(self.delta)
    def making_dict(self):
        if(len(self.dict_ex) == 0):
            self.dict_ex[date.today()] = {}
            self.dict_ex[f"Status{date.today()}"] = {}
        status = self.checkOnline()
        tme =  datetime.now().strftime("%H:%M") 
        dte = date.today()
        if(dte == self.dict_ex.keys[0] and len(self.dict_ex.keys[0]) != 0):
            self.dict_ex[dte][len(self.dict_ex[dte])] = tme
            self.dict_ex[f"Status{dte}"][len(self.dict_ex[f"Status{dte}"])] = status
        elif(dte != self.dict_ex.keys[0] and len(self.dict_ex.keys[0]) != 0):
            self.WriteToExcel(self.dict_ex[self.dict_ex.keys[0]],self.dict_ex[self.dict_ex.keys[1]], "report.xlsx",self.dict_ex.keys[0])
            self.dict_ex[dte] = {}
            self.dict_ex[f"Status{dte}"] = {}
            self.dict_ex[dte][len(self.dict_ex[dte])] = tme
            self.dict_ex[f"Status{dte}"][len(self.dict_ex[f"Status{dte}"])] = status
            
    


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