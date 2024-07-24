import asyncio
import logging

# from aiogram.filters.command import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.types import MessageReactionUpdated
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.bot_config import bot, dp
from handlers import vehicle, service, report
from scheduler.scheduler_func import send_vehicle_month_resume, send_vehicle_notify
from utils.constants import TIME_ZONE


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_vehicle_notify,
        'cron',
        day_of_week='mon-thu',
        hour=15,
        minute=0,
        timezone=TIME_ZONE
    )
    # напоминание о заказе техники в "пятницу"
    scheduler.add_job(
        send_vehicle_notify,
        'cron',
        day_of_week='fri',
        hour=11,
        minute=30,
        timezone=TIME_ZONE
    )
    scheduler.add_job(
        send_vehicle_month_resume,
        'cron',
        day='1',
        hour=10,
        minute=0,
        timezone=TIME_ZONE
    )
    scheduler.start()
    dp.include_routers(
        service.router,
        vehicle.router,
        report.router,
        vehicle.dialog,
    )
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        filename='logs_bot.log',
        level=logging.INFO,
        filemode='a',
        format='%(asctime)s - %(message)s',
        datefmt='%d.%m.%y %H:%M:%S',
        encoding='utf-8',
    )
    asyncio.run(main())
