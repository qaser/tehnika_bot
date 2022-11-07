import datetime as dt
import math

import utils.constants as const
from config.bot_config import bot
from config.mongo_config import vehicles
from config.telegram_config import CHAT_ID_GKS
from functions.word_conjugate import word_conjugate


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
    WORDS = ['Не будет', 'Нету', 'Нет']
    denial_count = 0
    month_now = dt.datetime.today().month
    year_now = dt.datetime.today().year
    previous_month = str(month_now - 1) if str(month_now) != '1' else '12'
    year = year_now if str(month_now) != '1' else (int(year_now) - 1)
    for word in WORDS:
        len_queryset = len(list(vehicles.find(
            {
                'confirm_comment': word,
                'date': {'$gt': f'01.{previous_month}.{year}'}
            }
        )))
        denial_count = denial_count + len_queryset
    location_resume = {}
    vehicle_resume = {}
    queryset = list(vehicles.find(
        {'date': {'$gt': f'01.{previous_month}.{year}'}}
    ))
    for loc in const.LOCATIONS:
        len_queryset = len(list(vehicles.find(
            {
                'location': loc,
                'date': {'$gt': f'01.{previous_month}.{year}'}
            }
        )))
        location_resume.update({loc: len_queryset})
    sorted_locations = sorted(
        location_resume.items(),
        key=lambda kv: kv[1],
        reverse=True
    )
    for veh in const.VEHICLES:
        len_queryset = len(list(vehicles.find(
            {
                'vehicle': veh,
                'date': {'$gt': f'01.{previous_month}.{year}'}
            }
        )))
        vehicle_resume.update({veh: len_queryset})
    sorted_vehicles = sorted(
        vehicle_resume.items(),
        key=lambda kv: kv[1],
        reverse=True
    )
    sum_doc = len(queryset)
    word_sum = word_conjugate(sum_doc)
    loc_max, loc_count_max = sorted_locations[0]
    word_loc = word_conjugate(loc_count_max)
    veh_max_1, veh_count_1 = sorted_vehicles[0]
    word_veh_1 = word_conjugate(veh_count_1)
    veh_max_2, veh_count_2 = sorted_vehicles[1]
    word_veh_2 = word_conjugate(veh_count_2)
    veh_max_3, veh_count_3 = sorted_vehicles[2]
    word_veh_3 = word_conjugate(veh_count_3)
    veh_max_last, veh_count_last = sorted_vehicles[-1]
    word_veh_last = word_conjugate(veh_count_last)
    accept_percent = math.ceil(100 - ((denial_count / sum_doc) * 100))
    message = (
        'Статистика за прошедший месяц.\n'
        f'Всего обработано {sum_doc} {word_sum} на спец. технику.\n'
        'Самое активное направление - '
        f'{loc_max} ({loc_count_max} {word_loc}).\n'
        'Самый популярный вид техники - '
        f'{veh_max_1} ({veh_count_1} {word_veh_1}).\n'
        f'На втором месте - {veh_max_2} ({veh_count_2} {word_veh_2}).\n'
        f'Замыкает тройку - {veh_max_3} ({veh_count_3} {word_veh_3}).\n'
        'Где-то в сторонке "рыдает" '
        f'{veh_max_last} - {veh_count_last} {word_veh_last}.\n\n'
        f'Примерно {accept_percent}% из всего количества заявок были одобрены.\n\n'
    )
    await bot.send_message(chat_id=CHAT_ID_GKS, text=message)
