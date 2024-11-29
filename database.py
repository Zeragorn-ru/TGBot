import sqlite3
from config import *


class DataBase:
    def __init__(self, file_name):
        self.cursor = None
        self.file = file_name

    def search_user(self, user_chat_id):
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            self.cursor.execute(f'''SELECT user_name FROM users WHERE chat_id = {user_chat_id}''')
            get = self.cursor.fetchall()
            self.connect.commit()
            for users in get:
                if users != "":
                    return True
            return False

    def add_user(self, message):
        with sqlite3.connect(self.file) as self.connect:
            self.cursor = self.connect.cursor()
            if self.search_user(message.chat.id):
                return
            self.cursor.execute(f'''INSERT INTO users (chat_id, user_name, currency, user_id) VALUES (?,?,?,?)''',
                                (message.chat.id, message.from_user.username, "usd", message.from_user.id))
            self.connect.commit()

def add_user(message):
    base = DataBase(BASE_NAME)
    base.add_user(message)