import requests
import json
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

def is_callback (dict):
    if 'callback_query' in dict:
        return True

def send_message (chatId, message):
    requests.post(sendURL + "?chat_id=" + str(chatId) + "&text=" + message)

def send_message_button (chatId, message, buttonJSON):
    requests.post(sendURL + "?chat_id=" + str(chatId) + "&reply_markup=" + buttonJSON + "&text=" + message)
    #print (sendURL + "?chat_id=" + str(chatId) + "&reply_markup=" + buttonJSON + "&text=" + message)

while True:
    newmessage = update (requestURL)

    if newmessage != False:

        if is_callback(newmessage) == True:
            userchatid = newmessage['callback_query']['message']['chat']['id']
            usertext = newmessage['callback_query']['message']['text']
            username = newmessage['callback_query']['message']['chat']['first_name']
            callback_data = newmessage['callback_query']['data']

            send_message (userchatid, "Callback from " + callback_data + ", pressed by " + username)

        else:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['chat']['first_name']

            if usertext.lower() == "button":
                buttonDict1 = {"text":"Knopf\n" + "hitest", "callback_data":"Knopf"}
                buttonDict2 = {"text":"Knopf2", "callback_data":"Knopf2"}
                buttonArr = {"inline_keyboard":[[buttonDict1, buttonDict2]]}
                send_message_button (userchatid, "Hi " + username, json.dumps(buttonArr))
            else:
                send_message(userchatid, "You said: " + usertext)

    sleep (1)
