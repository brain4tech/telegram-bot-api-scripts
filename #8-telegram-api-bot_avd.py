import requests
import json
from time import sleep
from os.path import dirname, abspath

global OFFSET
OFFSET = 0

botToken = ""

global requestURL
global sendURL

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage"

sendImageURL = "https://api.telegram.org/bot" + botToken + "/sendPhoto"
sendDocURL = "https://api.telegram.org/bot" + botToken + "/sendDocument"
sendVidURL = "https://api.telegram.org/bot" + botToken + "/sendVideo"
sendAudURL = "https://api.telegram.org/bot" + botToken + "/sendAudio"

def getcwd():
	cwd = dirname(abspath(__file__))
	cwd = cwd.replace("\\", "/")
	return cwd

imgpath = getcwd() + "/data/logo.png"
docpath = getcwd() + "/data/script.py"
vidpath = getcwd() + "/data/intro-HD.mp4"
audpath = getcwd() + "/data/intro-song.mp3"

def update(url):
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


def extract_result(dict):
    result_array = dict['result']

    if result_array == []:
        return False
    else:
        result_dic = result_array[0]
        return result_dic


def send_message_query(chatId, message):
    requests.post(sendURL + "?chat_id=" + str(chatId) + "&text=" + message)


def send_message(chatID, message):
    data = {'chat_id': chatID, 'text': message}

    response = requests.post(sendURL, data=data)
    print(response.request.url)
    print(response.request.headers)
    print(response.request.body)


def send_image(chatId, caption):
    print("Sending message ...")

    params = {'chat_id': chatId, 'caption': caption}
    img = {'image': open(imgpath, 'rb')}

    return requests.post(sendImageURL, params=params, files=img)


def send_document(chatId, caption):
    print("Sending message ...")

    params = {'chat_id': chatId, 'caption': caption}
    doc = {'document': open(docpath, 'rb')}

    return requests.post(sendDocURL, params=params, files=doc)


def send_video(chatId, caption):
    print("Sending message ...")

    params = {'chat_id': chatId, 'caption': caption}
    vid = {'video': open(vidpath, 'rb')}

    return requests.post(sendVidURL, params=params, files=vid)


def send_audio(chatId, caption):
    print("Sending message ...")

    params = {'chat_id': chatId, 'caption': caption}
    aud = {'audio': open(audpath, 'rb')}

    return requests.post(sendAudURL, params=params, files=aud)


while True:
    newmessage = update(requestURL)
    # print (newmessage)

    try:

        if newmessage != False:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['from']['first_name']

            if usertext.lower() == "hello":
                send_message(userchatid, "Hi " + username)
            elif usertext.lower() == "img":
                print(send_image(userchatid, "Das ist ein Bild").text)
            elif usertext.lower() == "doc":
                print(send_document(userchatid, "Das ist ein Dokument").text)
            elif usertext.lower() == "vid":
                print(send_video(userchatid, "Das ist ein Video").text)
            elif usertext.lower() == "aud":
                print(send_audio(userchatid, "Das ist eine Audio").text)
            else:
                send_message(userchatid, "You said: " + usertext)
                # break

    except Exception as e:
        print(e)

    sleep(1)
