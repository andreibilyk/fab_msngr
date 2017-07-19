# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
from flask import Flask, request
from SQLighter import SQLighter
import utils
import re

app = Flask(__name__)

db_worker = SQLighter()
network = {"1": "Сімейне право👨‍👩‍👧‍👦",
"11": 'Аліменти💰',
"111": 'Розмір аліментів🤓📊',
"112":'Заборгованість по аліментам😡⏳',
"113": 'Звільнення від сплати🤔',
"12":'Права батьків після розлучення👨‍👦👩‍👦',
"13":'Розлучення💔🙇🏼',
"14": 'Поділ майна🔪',
"15": 'Усиновлення👼🏼',
"16": 'Заповіт📜',
"17": 'Спадок🔗',
"2": 'Трудове право💳',
"21": 'Трудовий договір📄',
"22": 'Звільнення😔',
"23": 'Відпустка🏖',
"24": 'Відрядження🚊✈️',
"25": 'Праця неповнолітніх👶🏼',
"26": 'Лікарняний🏥👩🏼‍⚕️',
"264": 'Виплати💰',
"27": 'Випробування🔮',
"3": 'Право споживача🍞💇🏼‍♂️',
'31':'Права споживача📊💇🏼‍♂️',
'32':'Гарантія⚙️',
'33':'Виявлення недоліків🔬',
'34':'Заміна товару💰🛍',
'35':'Інтернет-магазин🖥',
'4':'Поліція👮🏼🚨',
'41':'Права поліцейських👮🏻‍♀️',
'42':'Пред’явлення посвідчення🙌🏻',
'43':'Стан сп’яніння🍸🚙',
'44':'Складання протоколу🖌👮🏼',
'45':'Штраф💰',
'46':'ДТП🚗',
}
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("postback"):
                 if messaging_event["postback"]["payload"] in network:
                     print((messaging_event["postback"]["payload"])[0])
                     if ((messaging_event["postback"]["payload"])[0] != "m"):
                      row = db_worker.select_row("'"+network.get(messaging_event["postback"]["payload"])+"'")
                      data = utils.generate_markup(row[2],messaging_event["postback"]["payload"],messaging_event["sender"]["id"])
                      send_message(messaging_event["sender"]["id"], data)
                 else:
                  if ((messaging_event["postback"]["payload"])[0] == "m"):
                   try:
                    row = db_worker.select_row("'"+network.get((messaging_event["postback"]["payload"])[4:])+"'")
                    data = utils.generate_markup_more(row[2],(messaging_event["postback"]["payload"])[4:],messaging_event["sender"]["id"])
                    send_message(messaging_event["sender"]["id"], data)
                   except BaseException as e :
                    print(str(e))
                  else:
                    print("answer is here")
                    row = db_worker.select_row2("'"+messaging_event["postback"]["payload"].encode('utf-8')+"'")
                    print(row)
                    print(messaging_event["postback"]["payload"].encode('utf-8'))
                    row[1] = re.sub(['<b>', '', row[1])
                    row[1] = re.sub(['</b>', '', row[1])
                    print(row[1])
                    data = utils.generate_answer(row[1],messaging_event["sender"]["id"])
                    send_message(messaging_event["sender"]["id"], data)
                if messaging_event.get("message"):  # someone sent us a message
                    try:
                     sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                     recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                     message_text = messaging_event["message"]["text"]  # the message's text
                    except BaseException:
                     print('error')
                    data = db_worker.select_main()
                    data["recipient"]["id"] = sender_id
                    send_message(sender_id, data)


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, data_to_send):

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps(data_to_send)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
