import datetime as dt

from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Radio, Select
from . import getters, states


async def on_vehicle_filter(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(states.ReportSG.BY_VEHICLE)


async def on_location_filter(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(states.ReportSG.BY_LOCATION)


def vehicle_getter(data) -> list[tuple[str, str]]:
    vehicles = data["vehicles"]
    # Создаем список кортежей (текст, ID)
    return [(vehicle, vehicle[:64]) for vehicle in vehicles]  # Ограничиваем длину ID


async def on_vehicle_selected(callback: CallbackQuery, select: Select,
                            manager: DialogManager, item_id: str):
    data = await getters.get_report_data(manager)
    selected_vehicle = item_id
    report_lines = data["result_by_vehicle"].get(selected_vehicle, [])

    report_text = (f"<b>Заявки на {selected_vehicle} {data['date']} "
                  f"по состоянию на {data['current_time']}(мск):</b>\n\n")
    report_text += "\n".join(report_lines)

    await callback.message.answer(
        text=report_text,
        parse_mode='HTML',
    )
    await manager.done()


async def on_vehicle_selected(callback: CallbackQuery, select: Select,
                            manager: DialogManager, item_id: str):
    data = await getters.get_vehicle_window_data(manager)
    selected_vehicle = item_id

    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date, 'vehicle': selected_vehicle}))

    report_lines = []
    for i in queryset:
        location = i.get('location')
        time = i.get('time')
        comment = i.get('comment')
        user = i.get('user')
        report_lines.append(f"{location} - {time.lower()}. \"{comment}\" ({user})")

    report_text = (f"<b>Заявки на {selected_vehicle} {data['date']} "
                  f"по состоянию на {data['current_time']}(мск):</b>\n\n")
    report_text += "\n".join(report_lines)

    await callback.message.answer(
        text=report_text,
        parse_mode='HTML',
    )
    await manager.done()

async def on_location_selected(callback: CallbackQuery, widget: Radio,
                             manager: DialogManager, item_id: str):
    data = await getters.get_location_report_data(item_id, manager)
    report_lines = []

    for location, orders in data["result_by_location"].items():
        report_lines.append(f"<b>{location}:</b>")
        report_lines.extend(orders)

    report_text = (f"<b>Заявки для {data['selected_location']} {data['date']} "
                  f"по состоянию на {data['current_time']}(мск):</b>\n\n")
    report_text += "\n".join(report_lines)

    await callback.message.answer(
        text=report_text,
        parse_mode='HTML',
    )
    await manager.done()
