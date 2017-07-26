# -*- coding: utf-8 -*-
import random
import re

urls = {
  "Сімейне право👨‍👩‍👧‍👦":"https://andreibilyk.com/simejnoje.jpg",
  "Трудове право💳":"https://andreibilyk.com/business.jpg",
  "Право споживача🍞💇🏼‍♂️":"https://andreibilyk.com/consumer.jpg",
  "Поліція👮🏼🚨":"https://andreibilyk.com/policia.jpg"
            }
url_stars = ["/static/1star.png","/static/2stars.png","/static/3stars.png"]
stars = ["Одна зірка🌟","Дві зірки🌟🌟","Три зірки🌟🌟🌟"]
def generate_markup(answers,callback,recipient_id,headline):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    print(callback)
    emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\u200d"
                u"\u23f3"#⏳
                u"\u2642"#♂
                u"\ufe0f"
                u"\u2699"#⚙️
                u"\U0001f913"
                u"\u2640"#♀
                u"\u2019"
                u"\u2708"#✈️
                u"\u2695"#⚕
                u"\U0001F914"
                u"\u2716"
                                   "]+", flags=re.UNICODE)
    data = {
        "recipient": {
            "id": recipient_id
        },
          "message": {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                        ],

        }
    }
}

    }

    # Склеиваем правильный ответ с неправильными
    list_items = []
    for item in answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    #random.shuffle(list_items)
    # Заполняем разметку перемешанными элементами

    if len(list_items)>3:
     data["message"]["attachment"]["payload"]["buttons"] = [
    {
    "title": "Більше",
    "type": "postback",
    "payload": "more"+callback
    }
    ]
    if len(callback)<2:
     data["message"]["quick_replies"] = [
          {
            "content_type":"text",
            "title":"Перелік сфер",
            "payload":"0"
          }
        ]
    else:
     data["message"]["quick_replies"] = [
          {
            "content_type":"text",
            "title":"Перелік сфер",
            "payload":"0"
          },
          {
            "content_type":"text",
            "title":"Назад",
            "payload":callback[:-1]
          },
        ]
    if headline in urls:
     data["message"]["attachment"]["payload"]["elements"].append(
     {
         "title": headline,
         "image_url": urls.get(headline)
     }
     )
    else:
     data["message"]["attachment"]["payload"]["top_element_style"] = "compact"
    print(data["message"]["attachment"]["payload"]["elements"])
    i = 0
    for item in list_items:
        i += 1
        if (i == 4 and urls.get(headline)) or (i == 5 and urls.get(headline) == None):
         return data
        if (len(callback + str(i)) <= 2 and (callback + str(i) != "31")) or (callback + str(i) == '111') or (callback + str(i) == '112') or (callback + str(i) == '113') or (callback + str(i) == '264'):
         print(item)
         data["message"]["attachment"]["payload"]["elements"].append(
                         {
                             "title": item,
                             "buttons": [
                                 {
                                     "title": "Переглянути",
                                     "type": "postback",
                                     "payload":callback + str(i)
                                 }
                             ]
                         }
          )
        else:
         print("here")
         data["message"]["attachment"]["payload"]["elements"].append(
                                   {
                                       "title": item,
                                       "buttons": [
                                           {
                                               "title": "Переглянути",
                                               "type": "postback",
                                               "payload":emoji_pattern.sub(r'', item)
                                           }
                                       ]
                                   }
                   )
    print(len(list_items))

    return data

def generate_markup_more(answers,callback,recipient_id):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\u200d"
                u"\u23f3"#⏳
                u"\u2642"#♂
                u"\ufe0f"
                u"\u2699"#⚙️
                u"\U0001f913"
                u"\u2640"#♀
                u"\u2019"
                u"\u2708"#✈️
                u"\u2695"#⚕
                u"\U0001F914"
                u"\u2716"
                                   "]+", flags=re.UNICODE)
    data = {
        "recipient": {
            "id": recipient_id
        },
          "message": {
    "attachment": {
        "type": "template",
        "payload": {
            "template_type": "list",
            "top_element_style": "compact",
            "elements": [
                        ],

        }
    }
}

    }

    # Склеиваем правильный ответ с неправильными
    list_items = []
    for item in answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    #random.shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    if len(callback)<2:
     data["message"]["quick_replies"] = [
          {
            "content_type":"text",
            "title":"Перелік сфер",
            "payload":"0"
          }
        ]
    else:
     data["message"]["quick_replies"] = [
          {
            "content_type":"text",
            "title":"Перелік сфер",
            "payload":"0"
          },
          {
            "content_type":"text",
            "title":"Назад",
            "payload":callback[:-1]
          },
        ]
    list_items = list_items[3:]
    i = 3
    for item in list_items:
        i += 1
        if i == 8:
         return data
        if (len(callback + str(i)) <= 2) or (callback + str(i) == '111') or (callback + str(i) == '112') or (callback + str(i) == '113') or (callback + str(i) == '264'):
          data["message"]["attachment"]["payload"]["elements"].append(
                         {
                             "title": item,
                             "buttons": [
                                 {
                                     "title": "Переглянути",
                                     "type": "postback",
                                     "payload":callback + str(i)
                                 }
                             ]
                         }
          )
        else:
         data["message"]["attachment"]["payload"]["elements"].append(
                                   {
                                       "title": item,
                                       "buttons": [
                                           {
                                               "title": "Переглянути",
                                               "type": "postback",
                                               "payload":emoji_pattern.sub(r'', item)
                                           }
                                       ]
                                   }
                   )
        print(len(list_items))
        if len(list_items)>4:
         data["message"]["attachment"]["payload"]["buttons"] = [
{
"title": "Більше",
"type": "postback",
"payload": "more"+callback
}
]
    return data

def generate_answer(answer,recipient_id):
 answer = answer + '''
Не знайшли відповідь?
 '''
 data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": answer
        }
    }
 data["message"]["quick_replies"] = [
      {
        "content_type":"text",
        "title":"Підключити оператора",
        "payload":"operator"
      },
      {
        "content_type":"text",
        "title":"Перелік сфер",
        "payload":"0"
      },
    ]
 return data

def generate_operator_end(recipient_id):
 data = {
     "recipient": {
     "id":recipient_id
     },
     "message":{
     "attachment":{
     "type":"template",
     "payload":{
     "template_type":"generic",
     "elements":[

             ]
             }
             }
             }
             }
 for x in range(2,-1):
  data["message"]["attachment"]["payload"]["elements"].append(
                {
                  "title":stars[x],
                  "image_url":"https://enigmatic-mesa-89892.herokuapp.com/"+url_stars[x],
                  "buttons":[{
                                "type":"postback",
                              "title":"Обрати оцінку",
                              "payload":"star"+str(x)
                                                }
                                              ]
                                            }
                )
 return data

def generate_file(file_url,recipient_id):
  data = {
  "recipient":{
    "id":recipient_id
  },
  "message":{
    "attachment":{
      "type":"file",
      "payload":{
        "url":file_url
      }
    }
  }
}
