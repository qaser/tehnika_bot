from aiogram_dialog import DialogManager
import datetime as dt
from config.mongo_config import vehicles
from .keyboards import SCROLLING_HEIGHT
from utils.constants import VEHICLES, DISPLAYED_LOCATIONS, GKS_GROUP


async def get_vehicles(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = vehicles.distinct('vehicle', {'date': date})
    return {
        'vehicles': [(VEHICLES.index(v), v) for v in queryset],
        'pager_enabled': True if len(queryset) > SCROLLING_HEIGHT else False
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
    # Проверяем, есть ли хотя бы одно значение из GKS_GROUP в queryset
    gks_group_locations = [loc for loc in GKS_GROUP if loc in queryset]
    # Если есть хотя бы одно из значений из GKS_GROUP, добавляем кнопку "ГКС"
    if gks_group_locations:
        locations_to_display.append('ГКС')
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
        'report_is_empty': True if len(queryset) == 0 else False,
        'report': report_text.strip(),
        'current_time': dt.datetime.today().strftime('%H:%M'),
        'date': date
    }


async def get_full_report_data(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    date_check = ctx.dialog_data.get('date')
    date = date_check if date_check else dt.datetime.today().strftime('%d.%m.%Y')
    # date = dt.datetime.today().strftime('%d.%m.%Y')
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
    del ctx.dialog_data['date']
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


async def get_stats_report(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    period = ctx.dialog_data['period']
    now = dt.datetime.now()
    # Определяем период для фильтрации
    if period == 'month':
        start_date = dt.datetime(now.year, now.month, 1)
        period_text = f'текущий месяц'
    elif period == 'year':
        start_date = dt.datetime(now.year, 1, 1)
        period_text = f'{now.year} год'
    else:  # lifetime
        start_date = None
        period_text = 'всё время'
    # Получаем общее количество заявок
    query = {'datetime': {'$gte': start_date}} if start_date else {}
    count_veh = vehicles.count_documents(query)
    # Генерируем статистику по направлениям и технике
    def generate_stats(group_field):
        pipeline = [
            {'$match': query} if start_date else {'$match': {}},
            {'$group': {'_id': f'${group_field}', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ]
        qs = vehicles.aggregate(pipeline)
        return '\n'.join([f"{item['_id']}: <b>{item['count']}</b>" for item in qs])
    text_location = generate_stats('location')
    text_vehicle = generate_stats('vehicle')
    # Формируем итоговый отчет
    report_text = (
        f'Статистика за {period_text}:\n'
        f'Всего заявок: <b>{count_veh}</b>\n\n'
        f'<u>Распределение по направлениям:</u>\n{text_location}\n\n'
        f'<u>Распределение по виду техники:</u>\n{text_vehicle}'
    )
    return {'report': report_text}
