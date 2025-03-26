from aiogram_dialog import DialogManager
import datetime as dt
from config.mongo_config import vehicles


DISPLAYED_LOCATIONS = [
    'АиМО',
    'ГКС',
    'ЛЭС',
    'Связь',
    'СЗК',
    'ЭВС',
    'ХМТРиСО'
]

# Группировка локаций для ГКС
GKS_GROUP = ['ГКС', 'КЦ-1,4', 'КЦ-2,3', 'КЦ-5,6', 'КЦ-7,8', 'КЦ-9,10']

async def get_main_window_data(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date}))
    return {
        "date": date,
        "current_time": dt.datetime.today().strftime('%H:%M'),
        "has_orders": len(queryset) > 0,
    }

async def get_vehicle_window_data(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date}))

    # Получаем уникальные типы техники
    vehicles_list = sorted(list(set(i.get('vehicle') for i in queryset)))

    return {
        "vehicles": [(v, v[:64]) for v in vehicles_list],
        "date": date,
        "current_time": dt.datetime.today().strftime('%H:%M'),
    }

async def get_location_window_data(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date}))

    # Получаем только те локации, которые есть в DISPLAYED_LOCATIONS
    existing_locations = set(i.get('location') for i in queryset)
    locations_to_display = [loc for loc in DISPLAYED_LOCATIONS if loc in existing_locations]

    return {
        "locations": locations_to_display,
        "date": date,
        "current_time": dt.datetime.today().strftime('%H:%M'),
    }

async def get_full_report_data(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date}))

    full_report_data = {}
    for i in queryset:
        vehicle = i.get('vehicle')
        location = i.get('location')
        time = i.get('time')
        comment = i.get('comment')
        user = i.get('user')

        if vehicle not in full_report_data:
            full_report_data[vehicle] = {}
        full_report_data[vehicle][location] = [time.lower(), comment, user]

    full_report_text = ""
    for vehicle, loc_list in full_report_data.items():
        part_message = ''
        for location, data_list in loc_list.items():
            time, comment, user = data_list
            text = '    <b>{}</b> - {}. "{}" <i>({})</i>\n'.format(
                location,
                time,
                comment,
                user,
            )
            part_message = '{}{}'.format(part_message, text)
        vehicle_part_text = '<u>{}</u>:\n{}'.format(vehicle, part_message)
        full_report_text = '{}{}\n'.format(full_report_text, vehicle_part_text)

    return {
        "full_report_text": full_report_text,
        "date": date,
        "current_time": dt.datetime.today().strftime('%H:%M'),
        "has_orders": len(queryset) > 0,
    }

async def get_location_report_data(selected_location: str, dialog_manager: DialogManager):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date}))

    # Определяем, какие локации нужно включить в отчет
    if selected_location == 'ГКС':
        locations_to_include = GKS_GROUP
    else:
        locations_to_include = [selected_location]

    # Фильтруем заявки по выбранным локациям
    filtered_orders = [
        i for i in queryset
        if i.get('location') in locations_to_include
    ]

    # Группируем по локациям для отчета
    result_by_location = {}
    for i in filtered_orders:
        location = i.get('location')
        vehicle = i.get('vehicle')
        time = i.get('time')
        comment = i.get('comment')
        user = i.get('user')

        if location not in result_by_location:
            result_by_location[location] = []
        result_by_location[location].append(
            f"{vehicle} - {time.lower()}. \"{comment}\" ({user})"
        )

    return {
        "result_by_location": result_by_location,
        "selected_location": selected_location,
        "date": date,
        "current_time": dt.datetime.today().strftime('%H:%M'),
    }
