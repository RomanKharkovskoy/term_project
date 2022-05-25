import json
import sqlite3 as sq

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

from face_functions import cleaning, discr_compare, extracting_faces, save_src
from top_secret import admin_token

class DataBase:
    """
    Base class that works with accessing the database 
    """
    def __init__(self, name):
        """
        Class constuctor that gives access to the database
        """
        self.name = name
        self.con = sq.connect(self.name)
        self.cur = self.con.cursor()
        
    def execute_query(self, query):
        """
        Query calling function
        """
        con = sq.connect(self.name)
        with con:
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            

    def insert_user(self, user_name, photo_discr):
        """
        Function that adds a person to the database
        """
        query = f'INSERT INTO users(user_name, photo_discr) VALUES ("{user_name}", "{photo_discr}")'
        self.execute_query(query)

    def delete_user(self, user_name):
        """
        Function that deletes a person from the database
        """
        query = f'DELETE FROM users WHERE user_name="{user_name}"'
        self.execute_query(query)

class TelegramNotifier:
    """
    Base class that works with TelegramBot API
    """
    def __init__(self, token, db_name):
        """
        Constructor of a class that uses inheritance 
        from a class with a database and calls bot functions
        """
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)
        self.db = DataBase(db_name)
        self.create_welcome_message()
        self.add_new_user_name()
        self.remove_user_name()

    def create_welcome_message(self):
        @self.dp.message_handler(commands=['start'])
        async def list_of_commands(message: types.Message):
            await message.reply(
                'Чтобы добавить нового пользователя напиши /add \n'
                'Чтобы удалить пользователя, напиши /delete'
            )

    def add_new_user_name(self):
        @self.dp.message_handler(commands=['add'], content_types=['text'])
        async def new_user_name(message: types.Message):
            await message.reply(
                'Сначала отправь имя пользователя, которого надо добавить'
            )
            username = message.text
            self.add_new_user_photo(username)
    
    def add_new_user_photo(self, username):
        @self.dp.message_handler(content_types=['photo'])
        async def new_user_photo(message: types.Message):
            destination = f'ideal_images/{username}.jpg'
            await message.photo[-1].download(destination_file=destination)
            discr = extracting_faces(f'ideal_images/{username}.jpg', username)
            self.db.insert_user(username, discr)
            await message.reply('Добавил этого человека в базу данных.')

    def remove_user_name(self):
        @self.dp.message_handler(commands=['remove'], content_types=['text'])
        async def remove_user(message: types.Message):
            await message.reply(
                'Отправь имя пользователя, которого надо удалить'
            )
            delete_user_name = message.text
            self.db.delete_user(delete_user_name)

if __name__ == '__main__':
    """
    Launching the bot
    """
    bot = TelegramNotifier(admin_token, 'db/table.db')
    executor.start_polling(bot.dp, skip_updates=True)