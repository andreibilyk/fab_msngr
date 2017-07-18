# -*- coding: utf-8 -*-
import random
import re



def generate_markup(answers,callback,recipient_id):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
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
                }

                        ]
        }
    }
}

    }
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
    # Склеиваем правильный ответ с неправильными
    list_items = []
    for item in answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    #random.shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    i = 0
    for item in list_items:
        i += 1
        if i == 4:
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
         data["elements"].append(
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
    return data
