import json
import sqlite3 as sq

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

from cmprg import cleaning, discr_compare, extracting_faces, save_src
from top_secret import token


class DataBase:
    def __init__(self, name):
        self.name = name

    def execute_query(self, query):
        con = sq.connect(self.name)
        with con:
            cur = con.cursor()
            cur.execute(query)
            con.commit()

    def selector(self):
        self.con = sq.connect(self.name)
        self.cur = self.con.cursor()

    def insert_user(self, user_name, photo_discr):
        query = f'INSERT INTO users(user_name, photo_discr) VALUES ("{user_name}", "{photo_discr}")'
        self.execute_query(query)

    def delete_user(self, user_name):
        query = f'DELETE FROM users WHERE user_name="{user_name}"'
        self.execute_query(query)

    def selecting_user(self):
        query = 'SELECT photo_discr, user_name FROM users'
        self.execute_query(query)


class TelegramNotifier:

    def __init__(self, token, db_name):
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)
        self.db = DataBase(db_name)
        self.create_welcome()
        self.create_new_user()
        self.delete_user()
        self.video_machine()

    def create_welcome(self):
        @self.dp.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply(
                              'Привет!\n'
                              'Чтобы добавить своё лицо в базу данных, отправь фотографию, на которой хорошо видно твоё лицо\n'
                              'Чтобы проверить кто находится на видео, отправь видео с данным человеком (бот отправит телеграмм аккаунт данного человека, если он есть в базе данных\n'
                              )

    def create_new_user(self):
        @self.dp.message_handler(commands=['new'])
        async def create_user(message: types.Message):
            await message.reply('Отправь своё фото, чтобы добавить его в базу данных.')
            self.work_with_photos()

    def work_with_photos(self):
        @self.dp.message_handler(content_types=['photo'])
        async def downloading_faces(message: types.Message):
            destination = f'ideal_images/{message.from_user.username}.jpg'
            await message.photo[-1].download(destination_file=destination)
            discr = extracting_faces(f'ideal_images/{message.from_user.username}.jpg', message.from_user.username)
            self.db.insert_user(message.from_user.username, discr)
            await message.reply('Добавил твоё фото в базу данных. Enjoy')

    def delete_user(self):
        @self.dp.message_handler(commands=['delete'])
        async def delete_user(message: types.Message):
            self.db.delete_user(message.from_user.username)
            await message.reply('Удалил тебя из базы данных. Bye')

    def video_machine(self):
        @self.dp.message_handler(commands=['video'])
        async def check_video(message: types.Message):
            await message.reply('Отправь кружок с лицом человеком и я дам ссылку на его телеграмм')
            self.work_with_videos()
    
    def work_with_videos(self):
        @self.dp.message_handler(content_types=[ContentType.VIDEO_NOTE])
        async def downloading_videos(message: types.Message):
            destination = f'images_to_compare/temp_video.mp4'
            await message.video_note.download(destination_file=destination)
            save_src("temp_video")
            await message.answer('Скачал твоё видео, сейчас сравню лицо с базой данных.')
            print(self.db.selector())
            for row in self.db.cur.execute('select photo_discr, user_name from users'):
                self.db.selecting_user()
                print(row[1])
                temp = json.loads(row[0])
                if discr_compare(temp) == [True]:
                    user = row[1]
                    await message.answer(f'На данном видео @{user}')
                    cleaning()
                    break

if __name__ == '__main__':
    bot = TelegramNotifier(token, 'db/base.db')
    executor.start_polling(bot.dp, skip_updates=True)
