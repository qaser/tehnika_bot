import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config.bot_config import bot, dp
from config.mongo_config import users
from config.telegram_config import MY_TELEGRAM_ID
from handlers.service import register_handlers_service
from handlers.vehicles import register_handlers_vehicle
from scheduler.scheduler_jobs import scheduler, scheduler_jobs
from texts.initial import INITIAL_TEXT

logging.basicConfig(
    filename='logs_bot.log',
    level=logging.INFO,
    filemode='a',
    format='%(asctime)s - %(message)s',
    datefmt='%d.%m.%y %H:%M:%S',
    encoding='utf-8'
)


# class PasswordCheck(StatesGroup):
#     waiting_password = State()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # user = message.from_user
    # check_user = users.find_one({'user_id': user.id})
    # if check_user is not None:
    #     await message.answer(INITIAL_TEXT)
    # else:
    #     await message.answer('Введите пароль')
    #     await PasswordCheck.waiting_password.set()
    user = message.from_user
    # проверяю есть ли пользователь в БД, если нет - добавляю
    check_user = users.find_one({'id': user.id})
    if check_user is None:
        users.insert_one({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'place_of_work': '',
        })
        await bot.send_message(
            chat_id=MY_TELEGRAM_ID,
            text=f'Добавлен новый пользователь в БД:\n{user.full_name}'
        )
    await message.answer(text=INITIAL_TEXT)


# @dp.message_handler(state=PasswordCheck.waiting_password)
# async def check_password(message: types.Message, state: FSMContext):
#     if message.text == PASSWORD:
#         await message.answer(INITIAL_TEXT)
#         await state.reset_state()
#         await state.reset_data()
#         users.insert_one({
#             'id': user.id,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'username': user.username,
#             'place_of_work': '',
#         })
#         await bot.send_message(
#             chat_id=MY_TELEGRAM_ID,
#             text=f'Добавлен новый пользователь в БД:\n{user.full_name}'
#         )
#     else:
#         await message.answer('Пароль неверный, повторите попытку')
#         return


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def delete_service_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def delete_message_left_member(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)


async def on_startup(_):
    scheduler_jobs()


if __name__ == '__main__':
    scheduler.start()
    register_handlers_service(dp)
    register_handlers_vehicle(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
