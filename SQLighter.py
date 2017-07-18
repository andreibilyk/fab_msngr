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
         return
