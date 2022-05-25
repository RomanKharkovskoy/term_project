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
        self.create_welcome()
        self.create_new_user()
        self.delete_user()

    def create_welcome(self):
        """
        Function decorator that gives access to commands /start and /help
        """
        @self.dp.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            """
            Welcome message after writing the command
            """
            await message.reply(
                              'Привет!\n'
                              'Чтобы добавить нового пользователя, напиши /new \n'
                              'Чтобы удалить пользователя напиши /delete'
                              )

    def create_new_user(self):
        """
        Function decorator that gives access to commands /new and /add
        """
        @self.dp.message_handler(commands=['new', 'add'])
        async def create_user(message: types.Message):
            """
            Function that responds to commands and associates 
            them with downloading faces from the sent video
            """
            await message.reply('Напиши имя аккаунта человека, которого надо добавить в базу данных.')
            self.get_user_name()

    def upload_photos(self, username):
        """
        Function decorator that reacts on photo types
        """
        @self.dp.message_handler(content_types=['photo', 'text'])
        async def downloading_faces(message: types.Message):
            """
            Function that downloads the received video and function that responds 
            to commands and associates them with downloading faces from the sent video
            """
            destination = f'ideal_images/{username}.jpg'
            await message.photo[-1].download(destination_file=destination)
            discr = extracting_faces(f'ideal_images/{username}.jpg', username)
            self.db.insert_user(username, discr)
            await message.reply('Добавил этого человека в базу данных.')

    def delete_user(self):
        """
        Function decorator that gives access to command /delete
        """
        @self.dp.message_handler(commands=['delete'])
        async def delete_user(message: types.Message):
            """
            Function that delete user from data base and reply this information.
            """
            await message.reply('Напиши имя пользователя, которого надо удалить')
            self.delete_user_name()

    def get_user_name(self):
        @self.dp.message_handler(content_types=['text'])
        async def get_user(message: types.Message):
            username = message.text
            await message.reply('Теперь отправь фото данного пользователя')
            self.upload_photos(username)

    def delete_user_name(self):
        @self.dp.message_handler(content_types='text')
        async def delete_user(message: types.Message):
            username = message.text
            self.db.delete_user(username)
            await message.reply('Удалил пользователя из базы данных')
            

if __name__ == '__main__':
    """
    Launching the bot
    """
    bot = TelegramNotifier(admin_token, 'db/table.db')
    executor.start_polling(bot.dp, skip_updates=True)