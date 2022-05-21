import json
import sqlite3 as sq

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

from face_functions import cleaning, discr_compare, extracting_faces, save_src
from top_secret import admin_token

class Database:
    def __init__(self, name):
        self.name = name

    def execute_query(self, query):
        con = sq.connect(self.name)
        with con:
            cur = con.cursor()
            cur.execute(query)
            con.commit()
    
    def insert_user(self, user_name, photo_discr):
        query = f'INSERT INTO users(user_name, photo_discr) VALUES ("{user_name}", "{photo_discr}")'
        self.execute_query(query)

    def delete_user(self, user_name):
        query = f'DELETE FROM users WHERE user_name="{user_name}"'
        self.execute_query(query)

class TelegramBot:
    def __init__(self, token, db_name):
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)
        self.db = Database(db_name)
        self.create_welcome()
        self.create_new_user()
        self.delete_user()

    def create_welcome(self):
        @self.dp.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply('Добро пожаловать в админ панель! \n'
            'Чтобы добавить пользователя напиши /add \n'
            'Чтобы удалить пользователя напиши /remove')

    def create_new_user(self):
        @self.dp.message_handler(commands=['new'])
        async def create_user(message: types.Message):
            await message.reply('Напиши имя пользователя')
            username = self.get_username
            self.work_with_photos()

    def get_username(self):
        @self.dp.message_handler(content_types=['text'])
        async def work_with_data(message: types.Message):
            username = message.text
            return username
        
    def work_with_photos(self):
        @self.dp.message_handler(content_types=['photo'])
        async def downloading_faces(message: types.Message):
            destination = f'ideal_images/{message.from_user.username}.jpg'
            await message.photo[-1].download(destination_file=destination)
            discr = extracting_faces(f'ideal_images/{message.from_user.username}.jpg', message.from_user.username)
            self.db.insert_user(message.from_user.username, discr)
            await message.reply('Добавил твоё фото в базу данных. Enjoy')
