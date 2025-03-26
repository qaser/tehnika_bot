from aiogram_dialog import DialogManager
import datetime as dt
from config.mongo_config import vehicles
from .keyboards import SCROLLING_HEIGHT
from utils.constants import VEHICLES


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


async def get_vehicles(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = vehicles.distinct('vehicle', {'date': date})
    return {
        'vehicles': [(VEHICLES.index(v), v) for v in queryset],
        'pager_enabled': True if len(queryset) >= SCROLLING_HEIGHT else False
    }


async def get_vehicle_report(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    date = dt.datetime.today().strftime('%d.%m.%Y')
    vehicle_id = ctx.dialog_data['vehicle']
    vehicle = VEHICLES[int(vehicle_id)]
    queryset = list(vehicles.find({'date': date, 'vehicle': vehicle}))
    vehicle_report_data = {}
    for i in queryset:
        location = i.get('location')
        time = i.get('time')
        comment = i.get('comment')
        user = i.get('user')
        if location not in vehicle_report_data:
            vehicle_report_data[location] = []
        vehicle_report_data[location].append([time.lower(), comment, user])
    report_text = f'<u>{vehicle}</u>:\n'
    for location, data_list in vehicle_report_data.items():
        for time, comment, user in data_list:
            report_text += f'    <b>{location}</b> - {time}. "{comment}" <i>({user})</i>\n'
    return {
        'vehicle': vehicle,
        'report_is_empty': True if len(queryset) == 0 else False,
        'report': report_text,
        'current_time': dt.datetime.today().strftime('%H:%M'),
        'date': date
    }


async def get_locations(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = vehicles.distinct('location', {'date': date})
    # Получаем только те локации, которые есть в DISPLAYED_LOCATIONS
    locations_to_display = [loc for loc in DISPLAYED_LOCATIONS if loc in queryset]
    return {
        'locations': [(DISPLAYED_LOCATIONS.index(v), v) for v in locations_to_display],
    }


async def get_location_report(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    date = dt.datetime.today().strftime('%d.%m.%Y')
    location_id = ctx.dialog_data['location']
    location = DISPLAYED_LOCATIONS[int(location_id)]
    locations = GKS_GROUP if location == 'ГКС' else [location]
    queryset = list(vehicles.find({'date': date, 'location': {'$in': locations}}))
    report_data = {}

    for entry in queryset:
        vehicle = entry.get('vehicle')
        location = entry.get('location')
        time = entry.get('time')
        comment = entry.get('comment', 'Без комментария')
        user = entry.get('user')

        if vehicle not in report_data:
            report_data[vehicle] = {}

        if location not in report_data[vehicle]:
            report_data[vehicle][location] = []

        report_data[vehicle][location].append((time.lower(), comment, user))

    report_text = ""

    for vehicle, locations_data in report_data.items():
        part_message = ''
        for loc, entries in locations_data.items():
            for time, comment, user in entries:
                part_message += f'    <b>{loc}</b> - {time}. "{comment}" <i>({user})</i>\n'

        report_text += f'<u>{vehicle}</u>:\n{part_message}\n'
    return {
        'location': location,
        'report_is_empty': True if len(queryset) == 0 else False,
        'report': report_text.strip(),
        'current_time': dt.datetime.today().strftime('%H:%M'),
        'date': date
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
    full_report_text = ''
    for vehicle, loc_list in full_report_data.items():
        part_message = ''
        for location, data_list in loc_list.items():
            time, comment, user = data_list
            text = '    <b>{}</b> - {}. "{}" <i>({})</i>\n'.format(location, time, comment, user)
            part_message = '{}{}'.format(part_message, text)
        vehicle_part_text = '<u>{}</u>:\n{}'.format(vehicle, part_message)
        full_report_text = '{}{}\n'.format(full_report_text, vehicle_part_text)
    return {
        'full_report_text': full_report_text,
        'date': date,
        'current_time': dt.datetime.today().strftime('%H:%M'),
        'has_orders': len(queryset) > 0,
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
            f'{vehicle} - {time.lower()}. \'{comment}\' ({user})'
        )

    return {
        'result_by_location': result_by_location,
        'selected_location': selected_location,
        'date': date,
        'current_time': dt.datetime.today().strftime('%H:%M'),
    }
