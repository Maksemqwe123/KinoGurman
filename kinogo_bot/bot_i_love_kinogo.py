from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from parser_films_kinogo_life2 import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

from KinoGurman.db_postgres import *
from buttons import *

import random

genre_kinogo_film = []

logging.basicConfig(filename='/KinoGurman/kinogo_bot/my_log_bot_kinogo.log', filemode='w+', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


bot = Bot(TOKEN_KINOGO)
dp = Dispatcher(bot, storage=MemoryStorage())

db = MyDBPostgres()


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    await message.answer('Привет, я бот который подскажет какой фильм можно посмотреть🍿🎬', reply_markup=user_kb)
    if not db.select_table('db_kinogo', message.from_user.id):
        db.insert_table_db_kinogo(message.from_user.id, message.from_user.username, "'" + strings_date + "'")


@dp.message_handler(commands='cancel', state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено❌')


@dp.callback_query_handler(text='films_buttons')
async def films_buttons(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    Parser(range(1, 10))

    all_info = list(zip(items, urls))
    for i in all_info:
        list_kinogo = f'Название: {i[0].strip()} \nСсылка: {i[1]}'
        spend.append(list_kinogo)

    mess = random.choice(spend)
    await bot.send_message(callback_query.from_user.id, f'{mess}', reply_markup=user_kb)


@dp.callback_query_handler(text='genre_film')
async def genre_film(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Выберите ваш любимый жанр фильма❤️‍🔥🎬🍿🏆', reply_markup=user_genre)


@dp.callback_query_handler(lambda call: True)
async def genre_film(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    store_buttons_clicked = callback_query.data
    db.update_db_kinogo(callback_query.from_user.id, store_buttons_clicked)

    genre_kinogo_film.append(store_buttons_clicked)

    ParserGenre(range(1, 4), genre_kinogo_film[0])
    all_info_genre = list(zip(items_genre, urls_genre))
    for i in all_info_genre:
        list_genre_kinogo = f'Название: {i[0].strip()} \nСсылка: {i[1]}'
        spend_genre.append(list_genre_kinogo)
    random_films = random.choice(spend_genre)
    random_films_2 = random.choice(spend_genre)
    random_films_3 = random.choice(spend_genre)

    await bot.send_message(callback_query.from_user.id, f'{random_films}')
    await bot.send_message(callback_query.from_user.id, f'{random_films_2}')
    await bot.send_message(callback_query.from_user.id, f'{random_films_3}', reply_markup=user_kb)

    await state.finish()

    items_genre.clear()
    urls_genre.clear()
    genre_kinogo_film.clear()
    spend_genre.clear()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
