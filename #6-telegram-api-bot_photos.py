import requests
import json
from time import sleep

global OFFSET
OFFSET = 0

botToken = ""

global requestURL
global sendURL

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage"
sendPhotoURL = "https://api.telegram.org/bot" + botToken + "/sendPhoto"

logopath = r"C:\Users\Jefta\Desktop\telegram-api-send-photo\b4t-design-logo.png"
imageURL = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"

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

def send_message_query (chatId, message):
    requests.post(sendURL + "?chat_id=" + str(chatId) + "&text=" + message)

def send_message (chatID, message):
    data = {'chat_id': chatID, 'text': message}

    response = requests.post(sendURL, data=data)
    print (response.request.url)
    print (response.request.headers)
    print (response.request.body)

def send_photo (chatId, photo, caption):
    print ("Sending message ...")

    params = {'chat_id': chatId, 'caption':"This is a caption"}
    img = {'photo': open(logopath, 'rb')}    

    requests.post(sendPhotoURL, params=params, files=img)
    


while True:
    newmessage = update (requestURL)
    #print (newmessage)

    try:

        if newmessage != False:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['from']['first_name']

            if usertext.lower() == "hello":
                send_message(userchatid, "Hi " + username)
            elif usertext.lower() == "logo":
                send_photo(userchatid, logopath, "Das ist das Logo")
            else:
                send_message(userchatid, "You said: " + usertext)
                #break
    
    except Exception as e:
        print(e)

    sleep (1)
