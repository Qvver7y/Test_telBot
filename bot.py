import json
import requests
from setuptools import Command



'''
available commands: /start, /help, /info


'''



#                                   <---------------- classes ---------------->





class Update_mes:
    def __init__(self, message,token):
        self.update_id = message['update_id']
        self.message_id = message['message']['message_id']
        self.from_id = message['message']['from']['id']
        self.from_firstName = message['message']['from']['first_name'] 
        self.from_lastName = message['message']['from']['last_name'] 
        self.chat_id = message['message']['chat']['id']
        self.text = message['message']['text']
        self.token = token
    def choose_ans(self):
        if(self.text == "/start"):
            self.startFunc()
        if(self.text == "/help"):
            self.helpFunc()
        if(self.text == "/info"):
            self.infoFunc()

    def infoFunc(self):
        data = {"chat_id": self.chat_id, "text": f"Hi,{self.from_firstName}!!\nThis is just test bot. But maybe it'll become something bigger!!"}
        self.send_ans("sendMessage",data)
    def helpFunc(self):
        data = {"chat_id": self.chat_id, "text": "available commands:\n/start\n/help\n/info"}
        self.send_ans("sendMessage", data)
    def startFunc(self):
        data = {"chat_id": self.chat_id, "text": "Hello world"}
        self.send_ans("sendMessage", data)        



    def send_ans(self, method_name,data = None):
        requests.post(f"https://api.telegram.org/bot{self.token}/{method_name}",data=data)

class Update:
    def __init__(self, res,token):
        self.message_mas = []
        self.token = token
        self.updates_id = -1
        for i in res['result']:
            new_el = Update_mes(i,self.token)
            self.message_mas.append(new_el)
        if(len(self.message_mas) > 0):
            self.updates_id = self.message_mas[-1].update_id + 1 # next update_id (for the next request)        





    
#                               <----------------- functions() ------------------>        





def get_updates(token, update_id=-1):
    data = {"offset":update_id}
    res = requests.post(f"https://api.telegram.org/bot{token}/getUpdates",data = data ).json()
    return Update(res,token)




def work(update_id, token):
    Updates = get_updates(token, update_id)
    for i in Updates.message_mas:
        i.choose_ans()
    return Updates.updates_id



def send_req(token, method_name,data = None):
   return requests.post(f"https://api.telegram.org/bot{token}/{method_name}",data=data)





def set_commands(token):
    datahelp = [{"command" : "/start", "description": "press to start bot"} , {"command" : "/help", "description":"bot's commands"}, 
        {"command" : "/info", "description": "learn more about this bot"}]
    datahelp = json.dumps(datahelp)
    data = {"commands" : datahelp}
    send_req(token, "setMyCommands",data = data )
    
def bot_config(token):
    set_commands(token)





#                                  <----------------- main() ------------------>





def main():
    f = open("token","r")
    token = f.readline()[0:-1]
    f.close()
    update_id = -1
    bot_config(token)
    while(1):
        update_id = work(update_id, token)

if __name__ == "__main__":
        main()