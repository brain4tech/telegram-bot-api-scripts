import requests
import json
from time import sleep

global OFFSET
OFFSET = 0

botToken = ""

global requestURL
global sendURL

standardURL = "http://api.telegram.org/bot" + botToken
requestURL = "http://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "http://api.telegram.org/bot" + botToken + "/sendMessage"

commandList = [{"command":"sayhi","description":"Says Hi!"},{"command":"like","description":"Drops a Like"},{"command":"help","description":"Should post a little bit of help, but doesn't"}]

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

# --- functions for command behaviour ---
def get_botCommands ():
    commandsraw = requests.get(standardURL + "/getMyCommands")
    commands = commandsraw.json()

    return commands

def set_botCommands (commandList):
    try:
        requests.post(standardURL + "/setMyCommands?commands=" + json.dumps(commandList))
    except Exception as e:
        return e

def is_command (messageData):
    if 'entities' in messageData:
        enitities = messageData['entities']
        entity = enitities[0]
        if entity['type'] == 'bot_command':
            spliced_command = splice_command(messageData['text'], entity['offset'], entity['length'])
            
            return spliced_command
    return False

def splice_command (text, offset, length):
    a = text[offset:]
    b = a[:length]

    return b

def handle_command (command, messageData):
    userchatid = messageData['message']['chat']['id']
    username = messageData['message']['chat']['first_name']

    if command == "/sayhi":
        send_message(userchatid, "Hi! I'm a Telegram-Bot. Everytime someone sends the command '/sayhi', I am forced to say 'Hi!' back. So, there you go:\nHi, " + username + "!")
    elif command == "/like":
        send_message(userchatid, "Go and like my latest YouTube-Video!")
    elif command == "/help":
        send_message(userchatid, "Nope.")
    else:
        send_message(userchatid, "Sorry, I don't understand that language.")


#print (get_botCommands())
set_botCommands(commandList)

while True:
    newmessage = update (requestURL)

    if newmessage != False:

        commandcheck = is_command(newmessage['message'])
        if commandcheck != False:
            handle_command(commandcheck, newmessage)
        
        #optional kann man das "Papageienspiel" in einen Else-Fall schieben
        else:
        
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['chat']['first_name']

            if usertext.lower() == "hello":
                send_message(userchatid, "Hi " + username)
                pass
            else:
                send_message(userchatid, "You said: " + usertext)
                pass

    sleep (1)
