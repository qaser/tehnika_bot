from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (Back, Button, Cancel, CurrentPage,
                                        NextPage, PrevPage, Row, Column, Calendar)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog
from . import getters, selected, states, keyboards


REPORT_IS_EMPTY = 'Заявки на технику пока отсутствуют'


async def exit_click(callback, button, dialog_manager):
    try:
        await dialog_manager.done()
        await callback.message.delete()
    except:
        pass


async def return_main_menu(callback, button, dialog_manager):
    await dialog_manager.switch_to(states.Report.CHOOSE_FILTER)


def main_window():
    return Window(
        Const('Выберите тип отчета:'),
        Button(
            Const('📋 Полный отчет'),
            id='full_report',
            on_click=selected.on_full_report_selected
        ),
        Button(
            Const('🚜 По типу техники'),
            id='by_vehicle',
            on_click=selected.on_vehicle_filter
        ),
        Button(
            Const('💼 По подразделению'),
            id='by_location',
            on_click=selected.on_location_filter
        ),
        Button(
            Const('📈 Статистика'),
            id='stats',
            on_click=selected.on_stats_menu
        ),
        Button(
            Const('📅 Архив заявок'),
            id='archive',
            on_click=selected.on_archive_calendar
        ),
        Button(Const('🔚 Выход'), on_click=exit_click, id='exit'),
        state=states.Report.CHOOSE_FILTER,
    )


def location_window():
    return Window(
        Const('Выберите подразделение:'),
        keyboards.location_buttons(selected.on_location_selected),
        Button(Const('🔙 Назад'), on_click=return_main_menu, id='main_menu'),
        state=states.Report.BY_LOCATION,
        getter=getters.get_locations,
    )


def vehicle_window():
    return Window(
        Const('Выберите тип техники:'),
        keyboards.vehicle_buttons(selected.on_vehicle_selected),
        Row(
            PrevPage(scroll='vehicle_pager', text=Format('<')),
            CurrentPage(scroll='vehicle_pager', text=Format('{current_page1} / {pages}')),
            NextPage(scroll='vehicle_pager', text=Format('>')),
            when='pager_enabled',
        ),
        Button(Const('🔙 Назад'), on_click=return_main_menu, id='main_menu'),
        state=states.Report.BY_VEHICLE,
        getter=getters.get_vehicles,
    )


def vehicle_filter_report_window():
    return Window(
        Const(REPORT_IS_EMPTY, when='report_is_empty'),
        Format('Заявки на технику по состоянию на {date} {current_time}(мск):\n'),
        Format('{report}'),
        Button(Const('🔙 Назад'), on_click=selected.on_vehicle_filter, id='vehicle_menu'),
        state=states.Report.VEHICLE_REPORT,
        getter=getters.get_vehicle_report,
    )


def location_filter_report_window():
    return Window(
        Const(REPORT_IS_EMPTY, when='report_is_empty'),
        Format('Заявки на технику по состоянию на {date} {current_time}(мск):\n'),
        Format('{report}'),
        Button(Const('🔙 Назад'), on_click=selected.on_location_filter, id='location_menu'),
        state=states.Report.LOCATION_REPORT,
        getter=getters.get_location_report,
    )


def stats_options_window():
    return Window(
        Const('Выберите период формирования статистики заявок:'),
        Column(
            Button(
                Const('За текущий месяц'),
                id='month',
                on_click=selected.on_stats_report
            ),
            Button(
                Const('За текущий год'),
                id='year',
                on_click=selected.on_stats_report
            ),
            Button(
                Const('За все время'),
                id='lifetime',
                on_click=selected.on_stats_report
            ),
            Button(
                Const('🔙 Назад'),
                on_click=return_main_menu,
                id='from_stats_to_main_menu',
            ),
        ),
        state=states.Report.CHOOSE_STATS_PERIOD,
    )


def stats_report_window():
    return Window(
        Format('{report}'),
        Button(
            Const('🔙 Назад'),
            on_click=selected.on_stats_menu,
            id='from_stats_report_to_stats_menu'
        ),
        state=states.Report.STATS_REPORT,
        getter=getters.get_stats_report,
    )


def archive_calendar_window():
    return Window(
        Const('Выберите дату:'),
        Calendar(
            id='calendar',
            on_click=selected.on_select_date,
        ),
        Button(
            Const('🔙 Назад'),
            on_click=return_main_menu,
            id='from_calendar_to_main_menu'
        ),
        state=states.Report.ARCHIVE_CALENDAR,
    )


def archive_report_window():
    return Window(
        Format('Заявки на технику на {date}:\n'),
        Format('{full_report_text}'),
        Button(
            Const('🔙 Назад'),
            on_click=selected.on_archive_calendar,
            id='from_archive_report_to_calendar'
        ),
        state=states.Report.ARCHIVE_REPORT,
        getter=getters.get_full_report_data,
    )
