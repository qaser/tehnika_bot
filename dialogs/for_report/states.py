from aiogram.filters.state import State, StatesGroup


class Report(StatesGroup):
    CHOOSE_FILTER = State()
    BY_VEHICLE = State()
    VEHICLE_REPORT = State()
    BY_LOCATION = State()
    LOCATION_REPORT = State()
    FULL_REPORT = State()
    CHOOSE_STATS_PERIOD = State()
    STATS_REPORT = State()
    # ARCHIVE_CALENDAR = State()
    # ARCHIVE_REPORT = State()
