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
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f'''INSERT INTO "{message.from_user.id}" (event_time, text) VALUES (?,?)''',
                                (time, text))
            self.connect.commit()

    def get_remind(self, user_id):
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f"""
            SELECT * FROM "{user_id}"
            """)
            get = self.cursor.fetchall()
            self.connect.commit()
            return get

    def rm_remind(self, user_id, id):
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f"""
            DELETE FROM "{user_id}" WHERE id = {id}
            """)
            self.connect.commit()

    def get_all_users(self):
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute("""
            SELECT user_id FROM users 
            """)
            get = self.cursor.fetchall()
            self.connect.commit()
            return get

def add_user(message):
    base = DataBase(BASE_NAME)
    base.add_user(message)

def add_remind(message, time, text):
    base = DataBase(BASE_NAME)
    base.add_remind(message, time, text)

def get_remind(message):
    base = DataBase(BASE_NAME)
    return base.get_remind(message)

def rm_remind(user_id, id):
    base = DataBase(BASE_NAME)
    base.rm_remind(user_id, id)

def get_all_users():
    base = DataBase(BASE_NAME)
    return base.get_all_users()
