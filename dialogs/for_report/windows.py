from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Radio, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog
from . import getters, selected, states


report_dialog = Dialog(
    Window(
        Const("Выберите тип отчета:"),
        Button(
            Const("Полный отчет"),
            id="full_report",
            on_click=selected.on_full_report_selected,
        ),
        Button(
            Const("По типу техники"),
            id="by_vehicle",
            on_click=selected.on_vehicle_filter,  # Используем отдельную функцию
        ),
        Button(
            Const("По подразделению"),
            id="by_location",
            on_click=selected.on_location_filter,  # Используем отдельную функцию
        ),
        Cancel(Const("Закрыть")),
        state=states.ReportSG.CHOOSE_FILTER,
        getter=getters.get_report_data,
    ),
    Window(
        Const("Выберите тип техники:"),
        Select(
            Format("{item[0]}"),  # Отображаемый текст
            id="s_vehicles",
            item_id_getter=lambda item: item[1],  # Используем второй элемент кортежа
            items="vehicles",
            on_click=selected.on_vehicle_selected,
        ),
        Back(Const("← Назад")),
        state=states.ReportSG.BY_VEHICLE,
        getter=getters.get_report_data,
    ),
    Window(
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
        state=states.ReportSG.BY_LOCATION,
        getter=getters.get_report_data,
    ),
)
