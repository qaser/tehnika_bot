from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Radio, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog
from . import getters, selected, states


async def on_exit(callback, button, dialog_manager):
    try:
        await dialog_manager.done()
        await callback.message.delete()
    except:
        pass


async def new_request(callback, button, dialog_manager):
    await dialog_manager.start(Vehicle.select_location, mode=StartMode.RESET_STACK)


def main_window():
    return Window(
        Const("Выберите тип отчета:"),
        Button(Const("Полный отчет"), id="full_report", on_click=selected.on_full_report_selected),
        Button(Const("По типу техники"), id="by_vehicle", on_click=selected.on_vehicle_filter),
        Button(Const("По подразделению"), id="by_location", on_click=selected.on_location_filter),
        Cancel(Const("Закрыть")),
        state=states.Report.CHOOSE_FILTER,
        getter=getters.get_main_window_data,
    )

def location_window():
    return Window(
        Const("Выберите подразделение:"),
        Radio(
            checked_text=Format("✓ {item}"),
            unchecked_text=Format("  {item}"),
            items="locations",
            item_id_getter=lambda x: x,
            id="location_radio",
            on_click=selected.on_location_selected,
        ),
        Back(Const("← Назад")),
        state=states.Report.BY_LOCATION,
        getter=getters.get_location_window_data,
    )

def vehicle_window():
    return Window(
        Const("Выберите тип техники:"),
        Select(
            Format("{item[0]}"),
            id="s_vehicles",
            item_id_getter=lambda item: item[1],
            items="vehicles",
            on_click=selected.on_vehicle_selected,
        ),
        Back(Const("← Назад")),
        state=states.Report.BY_VEHICLE,
        getter=getters.get_vehicle_window_data,
    )
