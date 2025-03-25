from aiogram_dialog import DialogManager
import datetime as dt
from config.mongo_config import vehicles


async def get_report_data(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date}))
    # Обрабатываем данные для отображения
    result_by_vehicle = {}
    result_by_location = {}
    full_report_data = {}  # Для полного отчета
    vehicles_list = []
    for i in queryset:
        vehicle = i.get('vehicle')
        location = i.get('location')
        time = i.get('time')
        comment = i.get('comment')
        user = i.get('user')
        # Группируем по технике
        if vehicle not in result_by_vehicle:
            result_by_vehicle[vehicle] = []
        result_by_vehicle[vehicle].append(f"{location} - {time.lower()}. \"{comment}\" ({user})")
        # Группируем по локациям
        if location not in result_by_location:
            result_by_location[location] = []
        result_by_location[location].append(f"{vehicle} - {time.lower()}. \"{comment}\" ({user})")
        # Для полного отчета (как в вашем оригинальном варианте)
        if vehicle not in full_report_data:
            full_report_data[vehicle] = {}
        full_report_data[vehicle][location] = [time.lower(), comment, user]
    # Формируем текст полного отчета
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
        "vehicles": [(v, v[:64]) for v in sorted(vehicles_list)],  # Кортежи с ограниченной длиной
        "locations": list(result_by_location.keys()),
        "result_by_vehicle": result_by_vehicle,
        "result_by_location": result_by_location,
        "full_report_text": full_report_text,
        "date": date,
        "current_time": dt.datetime.today().strftime('%H:%M'),
        "has_orders": len(queryset) > 0,
    }
