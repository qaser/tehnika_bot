import datetime as dt

from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Radio
from . import getters, states


async def on_vehicle_filter(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(states.ReportSG.BY_VEHICLE)

async def on_location_filter(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(states.ReportSG.BY_LOCATION)


async def on_filter_selected(callback: CallbackQuery, button: Button, manager: DialogManager):
    filter_type = button.widget_id
    if filter_type == "by_vehicle":
        await manager.switch_to(states.ReportStates.BY_VEHICLE)
    elif filter_type == "by_location":
        await manager.switch_to(states.ReportStates.BY_LOCATION)


async def on_vehicle_selected(callback: CallbackQuery, widget: Radio, manager: DialogManager, item_id: str):
    data = await getters.get_report_data(manager)
    selected_vehicle = item_id
    report_lines = data["result_by_vehicle"].get(selected_vehicle, [])

    report_text = f"<b>Заявки на {selected_vehicle} {data['date']} по состоянию на {data['current_time']}(мск):</b>\n\n"
    report_text += "\n".join(report_lines)

    await callback.message.answer(
        text=report_text,
        parse_mode='HTML',
    )
    await manager.done()

async def on_location_selected(callback: CallbackQuery, widget: Radio, manager: DialogManager, item_id: str):
    data = await getters.get_report_data(manager)
    selected_location = item_id
    report_lines = data["result_by_location"].get(selected_location, [])

    report_text = f"<b>Заявки для {selected_location} {data['date']} по состоянию на {data['current_time']}(мск):</b>\n\n"
    report_text += "\n".join(report_lines)

    await callback.message.answer(
        text=report_text,
        parse_mode='HTML',
    )
    await manager.done()


async def on_full_report_selected(callback: CallbackQuery, button: Button, manager: DialogManager):
    data = await getters.get_report_data(manager)

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
