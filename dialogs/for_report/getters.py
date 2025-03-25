from aiogram_dialog import DialogManager
import datetime as dt
from config.mongo_config import vehicles


async def get_report_data(dialog_manager: DialogManager, **kwargs):
    date = dt.datetime.today().strftime('%d.%m.%Y')
    queryset = list(vehicles.find({'date': date}))

    result_by_vehicle = {}
    vehicles_list = []

    for i in queryset:
        vehicle = i.get('vehicle')
        location = i.get('location')
        time = i.get('time')
        comment = i.get('comment')
        user = i.get('user')

        if vehicle not in result_by_vehicle:
            result_by_vehicle[vehicle] = []
            vehicles_list.append(vehicle)

        result_by_vehicle[vehicle].append(
            f"{location} - {time.lower()}. \"{comment}\" ({user})"
        )

    return {
        "vehicles": [(v, v[:64]) for v in sorted(vehicles_list)],  # Кортежи с ограниченной длиной
        "result_by_vehicle": result_by_vehicle,
        "date": date,
        "current_time": dt.datetime.today().strftime('%H:%M'),
        "has_orders": len(queryset) > 0,
    }
