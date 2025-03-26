from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup
from aiogram_dialog.widgets.text import Format

SCROLLING_HEIGHT = 6


def location_buttons(on_click):
    return Group(
        Select(
            Format('{item[1]}'),
            id='location',
            item_id_getter=lambda x: x[0],
            items='locations',
            on_click=on_click,
        ),
        width=2
    )


def vehicle_buttons(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[1]}'),
            id='vehicle',
            item_id_getter=lambda x: x[0],
            items='vehicles',
            on_click=on_click,
        ),
        id='vehicle_pager',
        width=1,
        height=SCROLLING_HEIGHT,
        hide_pager=True,
    )
