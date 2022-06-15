import requests
from time import sleep

global OFFSET
OFFSET = 0

botToken = ""

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage"
sendContactURL = "https://api.telegram.org/bot" + botToken + "/sendContact"

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

    data = {
        'chat_id': chatId,
        'text': message
        }
    
    requests.post(sendURL, data = data)


def send_contact (chatId, phone_number, first_name, last_name):
    data = {
        'chat_id': chatId,
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name
        }
    
    requests.post(sendContactURL, data = data)


while True:
    newmessage = update (requestURL)
    
    try:

        if newmessage != False:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['chat']['first_name']

            if usertext.lower() == "hello":
                send_message(userchatid, "Hi " + username)
            elif usertext.lower() == "contact":
                send_contact(userchatid, 49123456789, "Jefta", "Brain4Tech")
            else:
                send_message(userchatid, "You said: " + usertext)
    
    except Exception as e:
        print ("Es gab ein Fehler, aber das Programm ignoriert ihn:", e)


    sleep (1)