# -*- coding: utf-8 -*-
import psycopg2
import logging
class SQLighter:

    def __init__(self):
        self.connection = psycopg2.connect("dbname='d43gotq6lmbhn3' user='viqqyucuojusmv' host='ec2-54-83-205-71.compute-1.amazonaws.com' password='cc1458772d0f7f750214b407228469a6c6f009d1bff544a0837cbc2771eee540'")
        self.cursor = self.connection.cursor()

    def select_main(self):
        with self.connection:
         self.cursor.execute('SELECT * FROM user_interac WHERE id = 1')
         answers = (self.cursor.fetchall()[0])[2]
         print(answers)
         list_items = []
         for item in answers.split(','):
            list_items.append(item)
                     data = {
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
                              "subtitle":"Аліменти,права батьків 😀після розлучення,розлучення, поділ майна,jhjhhjjjhjhhjhjhjhjhj",
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
                            }
         for item in list_items:
             try:
              self.cursor.execute('SELECT * FROM user_interac WHERE user_answer = %s'% "'"+item+"'")
              answers = (self.cursor.fetchall()[0])[2]
              data["message"]["attachment"]["payload"]["elements"].append(
              {
                "title":item,
                "image_url":"https://andreibilyk.com/family.jpg",
                "subtitle":answers,
                "buttons":[
                           {
                            "type":"web_url",
                            "url":"https://www.w3schools.com",
                            "title":"View Website"
                            },{
                              "type":"postback",
                            "title":"Обрати сферу",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                                              }
                                            ]
                                          }
              )
             except BaseException:
              pass
         print(data)
         return
