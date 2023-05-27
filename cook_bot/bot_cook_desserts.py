# -*- coding: utf-8 -*-

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


from parser_desserts import *
from KinoGurman.db_postgres import *
from buttons import *

import random
import logging

logging.basicConfig(filename='//cook_bot/my_log_bot_cook.log', filemode='w+', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

list_name_desserts = []

db = MyDBPostgres()


bot = Bot(token=TOKEN_DESSERT)
dp = Dispatcher(bot, storage=MemoryStorage())


class SpecifyProducts(StatesGroup):
    state_products = State()


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message):
    await message.answer('Привет, я бот который подскажет какой десерт можно приготовить🥧🍦', reply_markup=user_kb)
    if not db.select_table('db_dessert', message.from_user.id):
        print(message.from_user.id, message.from_user.username, '"' + strings_date + '"')
        db.insert_table_db_dessert(message.from_user.id, message.from_user.username, "'" + strings_date + "'")


@dp.message_handler(commands='cancel', state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Действие отменено❌', reply_markup=user_kb)


@dp.callback_query_handler(text='dessert_product', state=None)
async def products_users(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           'Укажите продукты по которым вы хотите приготовить десерт🍯🌰🥛, '
                           'указывайте все через запетую в одном сообщении')
    time.sleep(2)
    await bot.send_message(callback_query.from_user.id, '❌Неправильно: Мука яйца_молоко. орехи')
    await bot.send_message(callback_query.from_user.id, '✅Правильно: Мука, мёд, молоко, орёхи, сгущёнка')

    await SpecifyProducts.state_products.set()


@dp.message_handler(state=SpecifyProducts.state_products)
async def products_specify(message: types.Message, state: FSMContext):
    text = message.text.encode("utf-8").decode('utf-8')
    ParserSelenium(text)
    all_info_dessert_selenium = list(zip(name_desserts_selenium, urls_selenium))

    for i in all_info_dessert_selenium[0:4]:
        list_dessert_selenium = f'Название: {i[0].strip()} \nСсылка: {i[1]}'
        await message.answer(list_dessert_selenium)
    await bot.send_message(message.from_user.id, 'Вот что можно приготовить🍩🍪', reply_markup=user_kb)

    name_desserts_selenium.clear()
    urls_selenium.clear()

    await state.finish()


@dp.callback_query_handler(text='choose_dessert')
async def dessert_users(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Выберите что вы хотите приготовить🍰🧁🥧🍦🍪',
                           reply_markup=user_dessert)


@dp.callback_query_handler(lambda call: True)
async def dessert_users(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    store_buttons_clicked = callback_query.data
    db.update_db_dessert(callback_query.from_user.id, store_buttons_clicked)
    values = name_urls.get(f'{store_buttons_clicked}')

    Parser(range(0, 4), f'{values}')

    all_info_dessert = list(zip(name_desserts, urls))

    for i in all_info_dessert:
        list_dessert = f'Название: {i[0]} \nСсылка: {i[1]}'
        dessert_random.append(list_dessert)

    dessert_message = random.choice(dessert_random)
    dessert_message_1 = random.choice(dessert_random)
    dessert_message_2 = random.choice(dessert_random)

    await bot.send_message(callback_query.from_user.id, dessert_message)
    await bot.send_message(callback_query.from_user.id, dessert_message_1)
    await bot.send_message(callback_query.from_user.id, dessert_message_2, reply_markup=user_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
