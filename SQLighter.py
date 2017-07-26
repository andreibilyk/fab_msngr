# -*- coding: utf-8 -*-
import psycopg2
import logging
class SQLighter:
    urls = {
  "1":"https://andreibilyk.com/simejnoje.jpg",
  "2":"https://andreibilyk.com/business.jpg",
  "3":"https://andreibilyk.com/consumer.jpg",
  "4":"https://andreibilyk.com/fb/policia.jpg"
            }
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
                              "id":''
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
         i = 1
         for item in list_items:
             try:
              self.cursor.execute('SELECT * FROM user_interac WHERE user_answer = %s'% "'"+item+"'")
              print('here1')
              answers = (self.cursor.fetchall()[0])[2]
              data["message"]["attachment"]["payload"]["elements"].append(
              {
                "title":item,
                "image_url":self.urls[str(i)],
                "subtitle":answers,
                "buttons":[{
                              "type":"postback",
                            "title":"Обрати сферу",
                            "payload":i
                                              }
                                            ]
                                          }
              )
              i += 1
             except BaseException:
              pass
         print(data)
         return data
    def select_row(self,answer):
                with self.connection:
                    self.cursor.execute('SELECT * FROM user_interac WHERE user_answer = %s '% answer)
                    return self.cursor.fetchall()[0]

    def select_row2(self,answer):
            with self.connection:
                try:
                 print(answer)
                 self.cursor.execute('SELECT * FROM user_interac WHERE user_answer LIKE %s '% str(answer))
                 return self.cursor.fetchall()[0]
                except BaseException as e:
                 print(str(e))
                 return

    def add_rank(self,rank,recipient_id,time_user):
              with self.connection:
                  try:
                   self.cursor.execute('INSERT INTO user_rank (time,rank,user_id) VALUES (%s,%s,%s)' % ("'"+str(time_user)+"'","'"+str(rank)+"'","'"+str(recipient_id)+"'"))
                   self.connection.commit()
                  except BaseException as e:
                   print(str(e))
                   return

    def get_rank():
        with self.connection:
            try:
             self.cursor.execute('SELECT * FROM user_rank')
             return self.cursor.fetchall()
            except BaseException as e:
             print(str(e))
             return
