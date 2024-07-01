from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove
from utils.constants import INITIAL_TEXT
from aiogram.fsm.context import FSMContext
from config.telegram_config import ADMIN_TELEGRAM_ID
from config.mongo_config import users


router = Router()


@router.message(Command('reset'))
async def reset_handler(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    await message.answer(
        'Текущее состояние бота сброшено',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(INITIAL_TEXT)


@router.message(Command('users'))
async def count_users(message: Message):
    user_id = message.from_user.id
    if user_id == int(ADMIN_TELEGRAM_ID):
        users_count = users.count_documents({})
        await message.answer(
            text=f'Количество пользователей в БД: {users_count}'
        )
    await message.delete()


@router.message(Command('log'))
async def send_logs(message: Message):
    user_id = message.from_user.id
    if user_id == int(ADMIN_TELEGRAM_ID):
        document = FSInputFile(path=r'logs_bot.log')
        await message.answer_document(document=document)
    await message.delete()
