# Diese Version des Basisscripts ist veraltet. Bitte verwende die zweite Version :D

import requests
from time import sleep

global OFFSET
OFFSET = 0

botToken = ""

global requestURL
global sendURL

requestURL = "http://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "http://api.telegram.org/bot" + botToken + "/sendMessage"

def update (url):
    global OFFSET

    try:
        update_raw = requests.get(url + "?offset=" + str(OFFSET))
        update = update_raw.json()
        result = extract_result(update)

        if result != False:
            OFFSET = result['update_id'] + 1
            return result
        else:
            return False

    except requests.exceptions.ConnectionError:
        pass

def extract_result (dict):
    result_array = dict['result']

    if result_array == []:
        return False
    else:
        result_dic = result_array[0]
        return result_dic


def send_message (chatId, message):
    requests.post(sendURL + "?chat_id=" + str(chatId) + "&text=" + message)


while True:
    newmessage = update (requestURL)
    
    try:

        if newmessage != False:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['chat']['first_name']

            if usertext.lower() == "hello":
                send_message(userchatid, "Hi " + username)
            else:
                send_message(userchatid, "You said: " + usertext)
    
    except Exception:
        pass

    sleep (1)
