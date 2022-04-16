import logging
import os
import sqlite3
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

from cmprg import extracting_faces
from top_secret import admin_token

bot = Bot(token = admin_token)
dp = Dispatcher(bot)
conn = sqlite3.connect('db/table.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(username: str, user_id: int, photo_dir: str):
    cursor.execute('INSERT INTO users (username, user_id, photo_dir) VALUES (?, ?, ?)', (username, user_id, photo_dir))
    conn.commit()

@dp.message_handler(commands='start')
async def start(message: types.Message):   
    await message.reply('Отправь имя человека в тг с @')

@dp.message_handler(content_types=['text'])
async def username(message: types.Message):
    f = open('admin_temp.txt', 'w')
    username = message.text
    f.write(username)
    f.close()

@dp.message_handler(content_types=['photo'])
async def add_users(message: types.Message):
    f = open('admin_temp.txt', 'r')
    username = f.readline()
    destination = f'ideal_images/{username}.jpg'
    await message.photo[-1].download(destination_file=destination)
    snames = extracting_faces(f'ideal_images/{username}.jpg', username)
    us_id = message.from_user.id
    db_table_val(username=username, user_id=us_id, photo_dir=snames)
    await message.answer(')')
    f.close()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)