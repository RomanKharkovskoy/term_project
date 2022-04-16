import logging
import sqlite3
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType

from cmprg import cleaning, discr_compare, extracting_faces, save_src
from top_secret import token

bot = Bot(token = token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('db/table.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(username: str, user_id: int, photo_dir: str):
    cursor.execute('INSERT INTO users (username, user_id, photo_dir) VALUES (?, ?, ?)', (username, user_id, photo_dir))
    conn.commit()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Привет дружище! Отправь свою фотографию, на которой хорошо видно лицо')

async def goodby(message: types.Message):
    await message.reply('До скорых встреч')

dp.register_message_handler(goodby, commands='by')

@dp.message_handler(content_types=['photo'])
async def add_photo(message: types.Message):
    destination = f'ideal_images/{message.from_user.username}.jpg'
    await message.photo[-1].download(destination_file=destination)
    snames= extracting_faces(f'ideal_images/{message.from_user.username}.jpg', message.from_user.username)
    us_id = message.from_user.id
    username = message.from_user.username
    db_table_val(username=username, user_id=us_id, photo_dir=snames)
    await message.answer('Добавил тебя в нашу базу данных :) \n Теперь отправь пожалуйста мне кружок, в котором будет видно твоё милое лицо)')

@dp.message_handler(content_types=[ContentType.VIDEO_NOTE])
async def video_machine(message: types.Message):
    await message.answer('⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧⬛️⬛️⬛️⬛️⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧🟧⬛️⬛️⬛️⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧🟧🟧⬛️⬛️⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧🟧🟧🟧⬛️⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧🟧🟧🟧🟧⬛️⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧🟧🟧🟧🟧🟧⬛️⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧🟧🟧🟧🟧🟧🟧⬛️')
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text='🟧🟧🟧🟧🟧🟧🟧🟧🟧🟧')
    destination = f'images_to_compare/temp_video.mp4'
    await message.video_note.download(destination_file=destination)
    save_src("temp_video")
    await message.answer('Скачал твоё видео, сейчас сравню лицо с базой данных.')  
    for row in cursor.execute('select photo_dir, username from users'):
        print(row[1])
        temp = json.loads(row[0])
        if discr_compare(temp) == [True]:
            user = row[1]
            await message.answer(f'На данном видео @{user}')
            cleaning()
            break

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





