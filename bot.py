from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from top_secret import token
import logging
import sqlite3
from screenshot_script import take_screenshot
import os

bot = Bot(token = token)
dp = Dispatcher(bot)
count = 0

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('db/table.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(username: str, user_id: int, photo_dir: str):
    cursor.execute('INSERT INTO users (username, user_id, photo_dir) VALUES (?, ?, ?)', (username, user_id, photo_dir))
    conn.commit()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Чтобы начать работу напиши мне "Привет"')

async def goodby(message: types.Message):
    await message.reply('До скорых встреч')

dp.register_message_handler(goodby, commands='by')

@dp.message_handler(content_types=[ContentType.VIDEO_NOTE])
async def vedio_machine(message: types.Message):
    await message.answer('Скачиваю полученный файл')
    destination = 'cache/video.mp4'
    us_id = message.from_user.id
    username = message.from_user.username
    photo_dir = f'{message.from_user.username}'
    db_table_val(username=username, user_id=us_id, photo_dir=photo_dir)
    await message.video_note.download(destination_file=destination)
    await message.answer('Скачал. Ищи себя в прошмандовках Азербайджана)')
    os.remove(f'{message.from_user.username}')
    take_screenshot(message.from_user.username)
    os.remove('cache/video.mp4')

@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    if message.text.lower() == "привет":
        await message.answer('Привет дружище! Добавил тебя в нашу базу данных :) \n Теперь отправь пожалуйста мне кружок, в котором будет видно твоё милое лицо)')
    
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





