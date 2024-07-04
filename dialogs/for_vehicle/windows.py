from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import (Back, Button, Cancel, CurrentPage,
                                        NextPage, PrevPage, Row)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput

from dialogs.for_vehicle.states import Vehicle

from . import getters, keyboards, selected


DONATE_NOTE = ('Уважаемый пользователь! Вы наверняка успели оценить удобство моего приложения.\n'
               'Я рад стараться для Вас и делать приложение ещё лучше. Однако сервера требуют '
               'оплаты, а новые фичи — разработки. Поэтому я был бы благодарен Вам за поддержку '
               'моего скромного труда. Ваша финансовая помощь поможет мне развиваться дальше и '
               'радовать Вас новыми обновлениями.')


async def on_exit(callback, button, dialog_manager):
    try:
        await dialog_manager.done()
        await callback.message.delete()
    except:
        pass


async def new_request(callback, button, dialog_manager):
    await dialog_manager.start(Vehicle.select_location, mode=StartMode.RESET_STACK)


def location_window():
    return Window(
        Const('Создание заявки на специальную технику.\nВыберите направление:'),
        keyboards.location_buttons(selected.on_chosen_location),
        Cancel(Const('🔚 Выход'), on_click=on_exit),
        state=Vehicle.select_location,
        getter=getters.get_locations
    )


def vehicle_window():
    return Window(
        Const('Выберите спец.технику из списка ниже:'),
        keyboards.vehicle_buttons(selected.on_chosen_vehicle),
        Row(
            PrevPage(scroll='vehicle_pager', text=Format('<')),
            CurrentPage(scroll='vehicle_pager', text=Format('{current_page1} / {pages}')),
            NextPage(scroll='vehicle_pager', text=Format('>')),
        ),
        Back(Const('🔙 Назад')),
        state=Vehicle.select_vehicle,
        getter=getters.get_vehicles
    )


def time_window():
    return Window(
        Const('Выберите необходимый период времени:'),
        keyboards.time_buttons(selected.on_chosen_time),
        Back(Const('🔙 Назад')),
        state=Vehicle.select_time,
        getter=getters.get_times
    )


def comment_window():
    return Window(
        Const('Если необходимо - можете добавить комментарий, '
              'или нажать на кнопку "Без комментария"'),
        TextInput(id='comments', on_success=selected.save_comments),
        Button(
            Const('✘ Без комментария'),
            id='no_comments',
            on_click=selected.no_comments,
        ),
        Back(Const('🔙 Назад')),
        state=Vehicle.input_comment
    )


def confirm_window():
    return Window(
        Const('<u>Вы ввели следующие данные:</u>\n'),
        Format('<b>Направление:</b> {location}'),
        Format('<b>Спец.техника:</b> {vehicle}'),
        Format('<b>Период:</b> {period}'),
        Format('<b>Комментарий:</b> {comment}'),
        Row(
            Back(Const('🔙 Назад')),
            Button(
                Const('✔️ Подтвердить'),
                id='confirm',
                on_click=selected.on_confirm,
            ),
            id='confirm_row'
        ),
        state=Vehicle.confirm,
        getter=getters.get_request
    )


def done_window():
    return Window(
        Const('Заявка сохранена'),
        Const('Вы можете сделать новую заявку или выйти из меню'),
        Button(
            Const('🆕 Новая заявка'),
            id='new_request',
            on_click=new_request,
        ),
        Button(
            Const('⭐ Поддержать разработчика'),
            id='donate',
            on_click=selected.on_donate_menu
        ),
        Cancel(Const('🔚 Выход'), on_click=on_exit),
        state=Vehicle.done
    )

def donate_window():
    return Window(
        Const(DONATE_NOTE),
        Button(
            Const('Перевести 1 ⭐'),
            id='donate_1',
            on_click=selected.on_donate
        ),
        Button(
            Const('Перевести 25 ⭐'),
            id='donate_25',
            on_click=selected.on_donate
        ),
        Button(
            Const('Перевести 50 ⭐'),
            id='donate_50',
            on_click=selected.on_donate
        ),
        Back(Const('🔙 Назад')),
        state=Vehicle.donate
    )
