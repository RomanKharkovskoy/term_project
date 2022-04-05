from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from top_secret import token
import logging

bot = Bot(token = token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply('Чтобы начать работу напиши мне "Привет"')

async def goodby(message: types.Message):
    await message.reply('До скорых встреч')

dp.register_message_handler(goodby, commands='by')

@dp.message_handler(content_types=[ContentType.VIDEO_NOTE])
async def vedio_machine(message: types.Message):
    await message.answer('Скачиваю полученный файл')
    destination = 'cache'
    await message.video_note.download(destination_dir=destination)
    await message.answer('Скачал')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


