from aiogram_dialog import DialogManager
from bson.objectid import ObjectId

from config.mongo_config import users
from dialogs.for_vehicle.states import Vehicle
from utils.constants import LOCATIONS, VEHICLES, PERIODS


async def get_locations(dialog_manager: DialogManager, **middleware_data):
    data = [(i, loc) for i, loc in enumerate(LOCATIONS)]
    return {'locations': data}


async def get_vehicles(dialog_manager: DialogManager, **middleware_data):
    data = [(i, veh) for i, veh in enumerate(VEHICLES)]
    return {'vehicles': data}


async def get_times(dialog_manager: DialogManager, **middleware_data):
    data = [(i, t) for i, t in enumerate(PERIODS)]
    return {'times': data}


async def get_request(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    return {
        'location': ctx.dialog_data['location'],
        'vehicle': ctx.dialog_data['vehicle'],
        'period': ctx.dialog_data['period'],
        'comment': ctx.dialog_data['comment']
    }
