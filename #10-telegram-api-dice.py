import requests
from time import sleep

global OFFSET
OFFSET = 0

botToken = ""

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage"
sendDiceURL = "https://api.telegram.org/bot" + botToken + "/sendDice"

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


def send_message (chatId, message, print_response = False):

    data = {
        'chat_id': chatId,
        'text': message
        }
    
    response = requests.post(sendURL, data = data)


def send_dice (chatId, emoji):
    data = {
        'chat_id': chatId,
        'emoji': emoji
        }
    
    requests.post(sendDiceURL, data = data)

while True:
    newmessage = update (requestURL)
    
    try:

        if newmessage != False:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['chat']['first_name']

            if usertext.lower() == "hello":
                send_message(userchatid, "Hi " + username)
            elif usertext.lower() == "dice":
                send_dice(userchatid, "🎰")
            else:
                send_message(userchatid, "You said: " + usertext)
    
    except Exception as e:
        print ("Es gab ein Fehler, aber das Programm ignoriert ihn:", e)


    sleep (1)
