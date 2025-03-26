import datetime as dt

from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Radio, Select
from . import getters, states
from config.mongo_config import vehicles


async def on_vehicle_filter(callback: CallbackQuery, button, manager: DialogManager):
    await manager.switch_to(states.Report.BY_VEHICLE)


async def on_location_filter(callback: CallbackQuery, button, manager: DialogManager):
    await manager.switch_to(states.Report.BY_LOCATION)


async def on_vehicle_selected(callback: CallbackQuery, button, manager: DialogManager, vehicle):
    context = manager.current_context()
    context.dialog_data.update(vehicle=vehicle)
    await manager.switch_to(states.Report.VEHICLE_REPORT)


async def on_location_selected(callback: CallbackQuery, button, manager: DialogManager, location):
    context = manager.current_context()
    context.dialog_data.update(location=location)
    await manager.switch_to(states.Report.LOCATION_REPORT)


async def on_full_report_selected(callback: CallbackQuery, button: Button, manager: DialogManager):
    data = await getters.get_full_report_data(manager)
    if not data["has_orders"]:
        await callback.message.answer("Заявки на технику пока отсутствуют")
        await manager.done()
        return
    final_message = '{}\n\n{}'.format(
        f'Заявки на технику {data["date"]} по состоянию на {data["current_time"]}(мск):',
        data["full_report_text"],
    )
    await callback.message.answer(
        text=final_message,
        parse_mode='HTML',
    )
    await manager.done()
