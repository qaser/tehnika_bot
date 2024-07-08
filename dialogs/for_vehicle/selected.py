import datetime as dt

from aiogram_dialog import DialogManager
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup

from dialogs.for_vehicle.states import Vehicle
from utils.constants import LOCATIONS, VEHICLES, PERIODS
from config.mongo_config import vehicles
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def on_chosen_location(callback, widget, manager: DialogManager, location_id):
    context = manager.current_context()
    context.dialog_data.update(location=LOCATIONS[int(location_id)])
    await manager.switch_to(Vehicle.select_vehicle)


async def on_chosen_vehicle(callback, widget, manager: DialogManager, vehicle_id):
    context = manager.current_context()
    context.dialog_data.update(vehicle=VEHICLES[int(vehicle_id)])
    await manager.switch_to(Vehicle.select_time)


async def on_chosen_time(callback, widget, manager: DialogManager, period_id):
    context = manager.current_context()
    context.dialog_data.update(period=PERIODS[int(period_id)])
    await manager.switch_to(Vehicle.input_comment)


async def save_comments(callback, widget, manager: DialogManager, comment):
    context = manager.current_context()
    context.dialog_data.update(comment=comment)
    await manager.switch_to(Vehicle.confirm)


async def no_comments(callback, widget, manager: DialogManager):
    context = manager.current_context()
    context.dialog_data.update(comment='Без комментария')
    await manager.switch_to(Vehicle.confirm)


async def on_confirm(callback, widget, manager: DialogManager):
    ctx = manager.current_context()
    date = dt.datetime.today()
    user = manager.event.from_user
    vehicles.insert_one(
        {
            'date': date.strftime('%d.%m.%Y'),
            'datetime': date,
            'user': user.full_name,
            'user_id': user.id,
            'location': ctx.dialog_data['location'],
            'vehicle': ctx.dialog_data['vehicle'],
            'time': ctx.dialog_data['period'],
            'comment': ctx.dialog_data['comment'],
            'confirm': False,
            'confirm_comment': '',
        }
    )
    await manager.switch_to(Vehicle.done)


async def on_donate_menu(callback, widget, manager: DialogManager):
    await manager.switch_to(Vehicle.donate)


async def on_donate(callback, widget, manager: DialogManager):
    context = manager.current_context()
    amount = int(widget.widget_id.split('_')[1])
    prices = [LabeledPrice(label="XTR", amount=amount)]
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Перевести {amount} XTR",
        pay=True
    )
    builder.button(
        text="Отменить перевод",
        callback_data="cancel"
    )
    builder.adjust(1)
    msg = await callback.message.answer_invoice(
        title='Добровольный перевод',
        description='Telegram Stars',
        prices=prices,
        provider_token="",
        payload=f"{amount}_stars",
        currency="XTR",
        reply_markup=builder.as_markup()
    )
    context.dialog_data.update(msg_id=msg.message_id)
