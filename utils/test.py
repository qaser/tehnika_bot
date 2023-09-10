import datetime as dt

import pymongo
# from config.telegram_config import MY_TELEGRAM_ID

client = pymongo.MongoClient('localhost', 27017)
db = client['tehnika_bot_db']
vehicles = db['vehicles']



qs = list(vehicles.find({}))
for v in qs:
    date = dt.datetime.strptime(v.get('date'), '%d.%m.%Y')
    vehicles.update_one({'_id': v.get('_id')}, {'$set': {'date': date}})
