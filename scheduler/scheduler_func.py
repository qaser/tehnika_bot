import datetime as dt
from dateutil.relativedelta import relativedelta

from config.bot_config import bot
from config.mongo_config import vehicles
from config.telegram_config import CHAT_ID_GKS, MY_TELEGRAM_ID
from aiogram.types import ParseMode


# функция напоминания о возможности зявить технику
async def send_vehicle_notify():
    date = dt.datetime.today().strftime('%d.%m.%Y')
    text_prefix = 'Добрый день. Напоминаю о возможности заявить технику.'
    text_suffix = '/zayavka'
    pipeline = [
        {'$match': {'date': date}},
        {'$group': {'_id': '$location', 'count': {'$sum': 1}}},
    ]
    res = list(vehicles.aggregate(pipeline))
    text = ''
    if len(res) != 0:
        for i in res:
            text = '{}{}\n'.format(text, i.get('_id'))
        final_text = f'На данный момент заявились:\n{text}'
    else:
        final_text = ''
    message = '{}\n{}\n{}'.format(text_prefix, final_text, text_suffix)
    await bot.send_message(chat_id=CHAT_ID_GKS, text=message)


# функция формирования и отправки статистики по технике
async def send_vehicle_month_resume():
    previous_month = dt.datetime.now() - relativedelta(months=1)
    count_veh = vehicles.count_documents({'date': {'$gt': previous_month}})
    text_location = res_generator('location', previous_month)
    text_vehicle = res_generator('vehicle', previous_month)
    summary_text = (f'За прошедший месяц ботом получено заявок: {count_veh}\n\n'
                    f'<u>Распределение по направлениям:</u>\n{text_location}\n'
                    f'<u>Распределение по виду транспорта:</u>\n{text_vehicle}')
    await bot.send_message(chat_id=CHAT_ID_GKS, text=summary_text, parse_mode=ParseMode.HTML)
    # await bot.send_message(chat_id=MY_TELEGRAM_ID, text=summary_text, parse_mode=ParseMode.HTML)


def res_generator(group, period):
    pipeline = [
        {'$match': {'date': {'$gt': period}}},
        {'$group': {'_id': f'${group}', 'count': {'$sum': 1}}},
        {'$sort': { 'count': -1}}
    ]
    qs = vehicles.aggregate(pipeline)
    res_text = ''
    for item in qs:
        name = item.get('_id')
        count = item.get('count')
        stats_text = f'{name}: <b>{count}</b>\n'
        res_text = f'{res_text}{stats_text}'
    return res_text
