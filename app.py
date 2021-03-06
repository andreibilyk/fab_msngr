# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
from flask import Flask, request
from SQLighter import SQLighter
import utils
import re
from flask import render_template
from functools import wraps
from flask import Response
import datetime


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
users = []

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'pravovyk' and password == 'H$sr^Ub8Bj-/kM}c'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/', methods=['GET'])
@requires_auth
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    #return "Hello world", 200
    return render_template('test.html', users=users)

@app.route('/ranks', methods=['GET'])
def ranks():
 data = db_worker.get_rank()
 print(data)
 new_data = [(item[0], datetime.datetime.fromtimestamp(
       int(item[1])/1000.00
   ).strftime('%Y-%m-%d         %H:%M:%S'), item[2],item[3]) for item in data]
 print(new_data)
 return render_template('ranks.html', ranks=new_data)



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
                      data = utils.generate_markup(row[2],messaging_event["postback"]["payload"],messaging_event["sender"]["id"],network.get(messaging_event["postback"]["payload"]))
                      send_message(messaging_event["sender"]["id"], data)
                 elif ((messaging_event["postback"]["payload"])[0] == "m"):
                  try:
                   row = db_worker.select_row("'"+network.get((messaging_event["postback"]["payload"])[4:])+"'")
                   data = utils.generate_markup_more(row[2],(messaging_event["postback"]["payload"])[4:],messaging_event["sender"]["id"])
                   send_message(messaging_event["sender"]["id"], data)
                  except BaseException as e :
                   print(str(e))
                 elif ((messaging_event["postback"]["payload"])[0] == "s"):
                  print(datetime.datetime.fromtimestamp(messaging_event["timestamp"]/1000.0))
                  print(datetime.datetime.now(),)
                  print(datetime.datetime.datetime.now())
                  print(str(int((messaging_event["postback"]["payload"])[4:])+1)+"   "+str(messaging_event["sender"]["id"])+"  "+ str(messaging_event["timestamp"]))
                  #db_worker.add_rank(str(int((messaging_event["postback"]["payload"])[4:])+1),messaging_event["sender"]["id"],messaging_event["timestamp"])
                  print("OK")
                 else:
                    row = db_worker.select_row2("'"+messaging_event["postback"]["payload"].encode('utf-8')+"'")
                    answer = row[1]
                    answer = re.sub('<b>', '', answer)
                    answer = re.sub('</b>', '', answer)
                    answer = re.sub('<i>', '', answer)
                    answer = re.sub('</i>', '', answer)
                    data = utils.generate_answer(answer,messaging_event["sender"]["id"])
                    send_message(messaging_event["sender"]["id"], data)
                if messaging_event.get("message"):  # someone sent us a message
                    if (messaging_event.get("message")).get("quick_reply"):
                     print("quick")
                     if (messaging_event["message"]["quick_reply"]["payload"] == "0"):
                      data = db_worker.select_main()
                      data["recipient"]["id"] = messaging_event["sender"]["id"]
                      send_message(messaging_event["sender"]["id"], data)
                     else:
                      try:
                       if (messaging_event["message"]["quick_reply"]["payload"] == "operator"):
                        params = {"fields":"first_name,last_name","access_token":os.environ["PAGE_ACCESS_TOKEN"]}
                        r = requests.get("https://graph.facebook.com/v2.6/"+messaging_event["sender"]["id"],params = params)
                        if r.status_code != 200:
                         log(r.status_code)
                         log(r.text)
                         return "ok", 200
                        data = json.loads(r.text)
                        print(data["first_name"])
                        users.append([data["first_name"]+" "+data["last_name"],messaging_event["sender"]["id"]])
                        print(users)
                        #here

                       else:
                        code = messaging_event["message"]["quick_reply"]["payload"]
                        print(code)
                        row = db_worker.select_row("'"+network.get(code)+"'")
                        data = utils.generate_markup(row[2],code,messaging_event["sender"]["id"],network.get(code))
                        send_message(messaging_event["sender"]["id"], data)
                      except BaseException as e :
                       print(str(e))
                     return "ok", 200
                    else:
                     print("оператор")


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

@app.route('/usersdel',methods=['GET', 'POST'])
def usersdel():
 print("Heyyy")
 print(request.get_data())
 data = utils.generate_operator_end(request.get_data())
 send_message(request.get_data(),data)
 for item in users:
  if item[1] == request.get_data():
   users.remove(item)
 print(users)
 return render_template("hello.html")


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
