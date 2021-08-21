import requests
from time import sleep
import json

global OFFSET
OFFSET = 0

botToken = ""

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage"
sendPollURL = "https://api.telegram.org/bot" + botToken + "/sendPoll"

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

def send_poll (chatId, question: str, options: list, is_anonymous=True, poll_type="regular",
                multiple_answers=False, correct_option=False, explanation="", open_period=0):
    data = {
        'chat_id': chatId,
        'question': question,
        'options': options,
        'is_anonymous': is_anonymous,
        'type': poll_type,
        'allows_multiple_answers': multiple_answers,
        'correct_option_id': correct_option,
        'explanation': explanation
        }
    
    if open_period > 5:
        data['open_period'] = open_period

    requests.post(sendPollURL, data=data)

while True:
    newmessage = update (requestURL)

    try:

        if newmessage != False:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['chat']['first_name']

            if usertext.lower() == "hello":
                send_message(userchatid, "Hi " + username)

            elif usertext.lower() == "poll":
                send_poll(userchatid, "This is a question", json.dumps(["Option 1", "Option 2"]))

            else:
                send_message(userchatid, "You said: " + usertext)
    
    except Exception as e:
        # print (newmessage)
        print ("Error:", e)


    sleep (1)
