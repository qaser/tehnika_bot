import datetime as dt

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.bot_config import bot
from config.mongo_config import offers, users
from config.telegram_config import CHAT_ID, MY_TELEGRAM_ID


class BotOffer(StatesGroup):
    waiting_for_offer = State()
    waiting_for_offer_confirm = State()


async def service_handler(message: types.Message):
    await bot.send_message(chat_id=CHAT_ID, text=SERVICE_TEXT)


async def service_end_handler(message: types.Message):
    await bot.send_message(chat_id=CHAT_ID, text=SERVICE_END_TEXT)


# обработка команды /reset - сброс клавиатуры и состояния
async def reset_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text='Сброс настроек бота выполнен, текущее действие отменено.',
        reply_markup=types.ReplyKeyboardRemove(),
    )


# обработка команды /user просмотр количества пользователей в БД
async def count_users(message: types.Message):
    queryset = list(users.find({}))
    users_count = len(queryset)
    final_text = ''
    for user in queryset:
        username = '{} {}'.format(user['first_name'], user['last_name'])
        final_text = '{}\n{}'.format(username, final_text)
    await message.answer(
        text=f'Количество пользователей в БД: {users_count}\n{final_text}'
    )


# обработка команды /offer - отзывы и предложения
async def bot_offer(message: types.Message):
    await message.answer(
        text=(
            f'Добрый день {message.from_user.full_name}.\n'
            'Если у Вас есть предложения по улучшению работы бота - '
            'напишите о них в следующем сообщении и мы сделаем всё '
            'возможное для их осуществления.'
        ),
    )
    await BotOffer.waiting_for_offer.set()


async def add_offer(message: types.Message, state: FSMContext):
    await state.update_data(offer=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Нет', 'Да')
    await message.answer(
        text='Вы точно хотите отправить отзыв о работе бота?',
        reply_markup=keyboard,
    )
    await BotOffer.waiting_for_offer_confirm.set()


async def confirm_offer(message: types.Message, state: FSMContext):
    if message.text.lower() not in ['нет', 'да']:
        await message.answer(
            'Пожалуйста, отправьте "Да" или "Нет"'
        )
        return
    if message.text.lower() == 'да':
        buffer_data = await state.get_data()
        offer = buffer_data['offer']
        user = message.from_user
        date = dt.datetime.today().strftime('%d.%m.%Y')
        offers.insert_one(
            {
                'date': date,
                'user_id': user.id,
                'offer': offer,
            }
        )
        await message.answer(
            ('Отлично! Сообщение отправлено.\n'
            'Спасибо за отзыв!'),
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.finish()
        await bot.send_message(
            chat_id=MY_TELEGRAM_ID,
            text=f'Получен новый отзыв от {user.full_name}:\n{offer}'
        )
    else:
        await message.answer(
            ('Хорошо. Отзыв не сохранен.\n'
             'Если необходимо отправить новый отзыв - нажмите /offer'),
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.reset_state()


def register_handlers_service(dp: Dispatcher):
    dp.register_message_handler(reset_handler, commands='reset', state='*')
    dp.register_message_handler(count_users, commands='users')
    dp.register_message_handler(bot_offer, commands='offer')
    dp.register_message_handler(add_offer, state=BotOffer.waiting_for_offer)
    dp.register_message_handler(
        confirm_offer,
        state=BotOffer.waiting_for_offer_confirm
    )
