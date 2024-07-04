from aiogram import F, Router
from aiogram.filters import Command
from aiogram_dialog import Dialog, DialogManager, StartMode
from config.bot_config import bot
from aiogram.types import Message

from config.telegram_config import ADMIN_TELEGRAM_ID
from dialogs.for_vehicle import windows
from dialogs.for_vehicle.states import Vehicle

router = Router()
dialog =  Dialog(
    windows.location_window(),
    windows.vehicle_window(),
    windows.time_window(),
    windows.comment_window(),
    windows.confirm_window(),
    windows.done_window(),
    windows.donate_window(),
)


@router.message(Command('vehicle'))
async def terms_request(message: Message, dialog_manager: DialogManager):
    await message.delete()
    # Important: always set `mode=StartMode.RESET_STACK` you don't want to stack dialogs
    await dialog_manager.start(Vehicle.select_location, mode=StartMode.RESET_STACK)


# команда /zayavka - перенаправит юзера к боту для заказа техники
@router.message(Command('zayavka'))
async def redirect_vehicle(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Для начала нажмите /vehicle'
    )
    await bot.delete_message(message.chat.id, message.message_id)


@router.pre_checkout_query()
async def on_pre_checkout_query(pre_checkout_query, l10n):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(message, l10n):
    await message.answer(
        ('Огромное спасибо!\nВаш айди транзакции:\n'
         f'{message.successful_payment.telegram_payment_charge_id}\n'
         'Сохраните его, если вдруг сделать возврат в будущем 😢'),
        message_effect_id="5104841245755180586",
    )
    await bot.send_message(
        chat_id=ADMIN_TELEGRAM_ID,
        text='Получен донат!!!',
        message_effect_id="5104841245755180586",
    )


@router.callback_query(F.data.startswith('cancel'))
async def cancel(callback, dialog_manager: DialogManager):
    try:
        await callback.message.delete()
    except:
        pass
