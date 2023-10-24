import datetime as dt
from dateutil.relativedelta import relativedelta

import pymongo
# from config.telegram_config import MY_TELEGRAM_ID

client = pymongo.MongoClient('localhost', 27017)
db = client['tehnika_bot_db']
vehicles = db['vehicles']


qs = vehicles.find({})
for v in list(qs):
    datetime_object = dt.datetime.strptime(v.get('date'), '%d.%m.%Y')
    vehicles.update_one(
        {'_id': v.get('_id')},
        {'$set': {'date': datetime_object}}
    )


# previous_month = dt.datetime.now() - relativedelta(month=1)
# pipeline = [
#     # {'$match': {'date': {'$gt': previous_month}}},
#     {'$group': {'_id': f'$vehicle', 'count': {'$sum': 1}}},
#     {'$sort': { 'count': -1}}
# ]
# qs = vehicles.aggregate(pipeline)
# res_text = ''
# for item in qs:
#     # print(item)
#     name = item.get('_id')
#     count = item.get('count')
#     stats_text = f'{name}: <b>{count}</b>\n'
#     res_text = f'{res_text}{stats_text}'
# print(res_text)


def send_vehicle_month_resume():
    previous_month = dt.datetime.now() - relativedelta(months=1)
    count_veh = vehicles.count_documents({'date': {'$gt': previous_month}})
    text_location = res_generator('location', previous_month)
    text_vehicle = res_generator('vehicle', previous_month)
    summary_text = (f'За прошедший месяц ботом получено заявок: {count_veh}\n\n'
                    f'<u>Распределение по направлениям:</u>\n{text_location}\n'
                    f'<u>Распределение по виду транспорта:</u>\n{text_vehicle}')
    print(summary_text)

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


send_vehicle_month_resume()
