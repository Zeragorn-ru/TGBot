import sqlite3
from time import strptime

from config import *
import datetime


class DataBase:
    def __init__(self, file_name):
        self.cursor = None
        self.file = file_name

    def search_user(self, message):
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f'''SELECT user_name FROM users WHERE user_id = {message.from_user.id}''')
            get = self.cursor.fetchall()
            self.connect.commit()
            for users in get:
                if users != "":
                    return True
            return False

    def add_user(self, message):
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            if self.search_user(message):
                return
            self.cursor.execute(f'''INSERT INTO users (user_name, currency, user_id, admin) VALUES (?,?,?,?)''',
                                (message.from_user.username, "usd", message.from_user.id, 0))
            self.connect.commit()
            self.cursor.executecursor.execute(f"""
            CREATE TABLE "{message.from_user.id}" ("id" INTEGER PRIMARY KEY, "event_time" TEXT, "text" TEXT)
            """)
            self.connect.commit()

    def add_remind(self, message, time, text):
        print(strptime(time, "%Y.%m.%d %H:%M:%S"))
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f'''INSERT INTO "{message.from_user.id}" (event_time, text) VALUES (?,?)''',
                                (time, text))
            self.connect.commit()

def add_user(message):
    base = DataBase(BASE_NAME)
    base.add_user(message)

def add_remind(message, time, text):
    base = DataBase(BASE_NAME)
    base.add_remind(message, time, text)