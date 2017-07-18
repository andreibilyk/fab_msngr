# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)



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

                if messaging_event.get("message"):  # someone sent us a message
                    try:
                     sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                     recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                     message_text = messaging_event["message"]["text"]  # the message's text
                    except BaseException:
                     print('error')

                    params = {
                    }
                    headers = {
                        "Content-Type": "application/json"
                    }
                    data = json.dumps({
                      "setting_type": "domain_whitelisting",
                      "whitelisted_domains": [
                        "https://www.andreibilyk.com"
                      ],
                      "domain_action_type": "add"
                    })
                    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings?access_token=EAAMtHsSYxe8BAAT7hMYsdPc6OZBPLYKSy6nAgY7NfDJVQNzBzWLyhYZBipsDFm1W1uxrA9LlZC09ZBzN5BQEwXCabn4VmG36SCj2EUbSK8N0QB8gcBf8kZApWDxndtQEmQpFtbatLeIZAiloIKQqnskXa7I8vzTgvdjIOD6chFGZAfw3qnxUuPVbE3w20bW3zsBMb2034TJwQZDZD", params=params, headers=headers, data=data)
                    if r.status_code != 200:
                        print(r.status_code)
                        print(r.text)
                    print(r.status_code)
                    send_message(sender_id, "roger that!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
          "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Сімейне право",
            "image_url":"https://andreibilyk.com/family.jpg",
            "subtitle":"Аліменти,права батьків після розлучення,розлучення, поділ майна",
            "buttons":[
              {
                "type":"web_url",
                "url":"https://www.w3schools.com",
                "title":"View Website"
              },{
                "type":"postback",
                "title":"Start Chatting",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              }
            ]
          },
          {
           "title":"Welcome to Peter\'s Hats",
           "image_url":"https://www.w3schools.com/css/trolltunga.jpg",
           "subtitle":"We\'ve got the right hat for everyone.",
           "default_action": {
             "type": "web_url",
             "url": "https://www.w3schools.com",
             "messenger_extensions": 'true',
             "webview_height_ratio": "tall",
             "fallback_url": "https://www.w3schools.com"
           },
           "buttons":[
             {
               "type":"web_url",
               "url":"https://www.w3schools.com",
               "title":"View Website"
             },{
               "type":"postback",
               "title":"Start Chatting",
               "payload":"DEVELOPER_DEFINED_PAYLOAD"
             }
           ]
         }
        ]
      }
    }
  }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
          "message": {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": "Classic T-Shirt Collection",
                    "image_url": "https://www.w3schools.com/css/trolltunga.jpg",
                    "subtitle": "See all our colors",
                    "buttons": [
                        {
                            "title": "View",
                            "type": "postback",
                            "payload":"s"
                        }
                    ]
                },
                {
                    "title": "Classic White T-Shirt",
                    "subtitle": "100% Cotton, 200% Comfortable",
                    "buttons": [
                        {
                            "title": "Shop Now",
                            "type": "postback",
                            "payload":"s"
                        }
                    ]
                },
                {
                            "title": "Classic Brown T-Shirt",
                            "image_url": "https://andreibilyk.com/family.jpg",
                            "subtitle": "100% Cotton, 200% Comfortable",
                            "buttons": [
                                {
                                    "title": "Shop Now",
                                    "type": "postback",
                                    "payload":"s"
                                }
                            ]
                        }
                        ],


             "buttons": [
                {
                    "title": "View More",
                    "type": "postback",
                    "payload": "payload"
                }
            ]
        }
    }
}

    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
  "message":{
    "text":"Pick a color:",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Red",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
      },
      {
        "content_type":"text",
        "title":"Green",
        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
      }
    ]
  }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
