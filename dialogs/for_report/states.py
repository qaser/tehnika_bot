from aiogram.filters.state import State, StatesGroup


class Report(StatesGroup):
    CHOOSE_FILTER = State()
    BY_VEHICLE = State()
    BY_LOCATION = State()
    FULL_REPORT = State()
