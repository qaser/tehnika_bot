from aiogram.filters.state import State, StatesGroup


class Vehicle(StatesGroup):
    select_location = State()
    select_vehicle = State()
    select_time = State()
    input_comment = State()
    confirm = State()
    done = State()
    donate = State()
