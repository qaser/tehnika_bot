import datetime as dt

from aiogram import F, Router
from aiogram.filters import Command
from aiogram_dialog import Dialog, DialogManager, StartMode
from aiogram.types import Message
from dialogs.for_report.states import ReportStates


router = Router()


@router.message(Command("report"))
async def cmd_report(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ReportStates.CHOOSE_FILTER)

# @router.message(Command('report'))
# async def send_vehicle_report(message: Message):
#     date = dt.datetime.today().strftime('%d.%m.%Y')
#     date_time = dt.datetime.today().strftime('%H:%M')
#     queryset = list(vehicles.find({'date': date}))
#     if len(queryset) == 0:
#         final_message = 'Заявки на технику пока отсутствуют'
#     else:
#         result = {}
#         for i in queryset:
#             if result.get(i.get('vehicle')) is None:
#                 result[i.get('vehicle')] = {}
#             result[i.get('vehicle')][i.get('location')] = [
#                 i.get('time'),
#                 i.get('comment'),
#                 i.get('user'),
#             ]
#         mess = ''
#         for vehicle, loc_list in result.items():
#             part_message = ''
#             for location, data_list in loc_list.items():
#                 time, comment, user = data_list
#                 text = '    <b>{}</b> - {}. "{}" <i>({})</i>\n'.format(
#                     location,
#                     time.lower(),
#                     comment,
#                     user,
#                 )
#                 part_message = '{}{}'.format(part_message, text)
#             vehicle_part_text = '<u>{}</u>:\n{}'.format(vehicle, part_message)
#             mess = '{}{}\n'.format(mess, vehicle_part_text)
#         final_message = '{}\n\n{}'.format(
#             f'Заявки на технику {date} по состоянию на {date_time}(мск):',
#             mess,
#         )
#     await message.answer(text=final_message)
#     await bot.delete_message(message.chat.id, message.message_id)
