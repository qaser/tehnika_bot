from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import Dialog, DialogManager, StartMode
from aiogram.types import Message
from dialogs.for_report.states import Report
from dialogs.for_report import windows


router = Router()
dialog =  Dialog(
    windows.main_window(),
    windows.location_window(),
    windows.vehicle_window(),
    windows.vehicle_filter_report_window(),
    windows.location_filter_report_window(),
    windows.stats_options_window(),
    windows.stats_report_window(),
    windows.archive_calendar_window(),
    windows.archive_report_window(),
)


@router.message(Command('report'))
async def cmd_report(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Report.CHOOSE_FILTER, mode=StartMode.RESET_STACK)
