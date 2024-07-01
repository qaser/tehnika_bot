from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode
from config.bot_config import bot

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
