from py_librus_api import Librus
import pprint
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

librus = Librus()
bot = Bot(token='5635042225:AAF0s3TxMNfubADmg0IpjEOWv7kNUZA1EvA')
dp = Dispatcher(bot, storage=MemoryStorage())
grades_button = types.KeyboardButton('Показати оцінки')
user_button = types.KeyboardButton('Показати профіль учня')

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(grades_button, user_button)

@dp.message_handler(commands=['start'])
async def start_command(message:  types.Message):
    await message.reply('Dzień dobry! Я - бот, який допоможе тобі користуватись лібрусом в телеграмі!')

@dp.message_handler(commands=['login'])
async def process_login_command(message: types.Message, state: FSMContext):
    await message.reply("Впишіть свій логін")
    await state.set_state('username')

@dp.message_handler(state='username')
async def process_username(message: types.Message, state: FSMContext):
    global user
    user = message.text
    await message.reply('Впишіть свій пароль')
    await state.set_state('password')

@dp.message_handler(state='password')
async def process_password(message: types.Message, state: FSMContext):
    global password
    password = message.text
    await message.reply('Входимо в лібрус...')
    print(user + '' + password)
    await state.set_state('logging_in')

@dp.message_handler(state='logging_in')
async def log_in_librus(message: types.Message, state: FSMContext):
    while not librus.logged_in:
        if not librus.login(user, password):
            await message.reply('Невдалий вхід! Перевірьте пароль та логін, і спробуйте ще раз.')
            break
        else:
            await message.reply('Вдалий вхід! :)')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
