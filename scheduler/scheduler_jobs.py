from apscheduler.schedulers.asyncio import AsyncIOScheduler

import utils.constants as const
from scheduler.scheduler_func import (send_vehicle_month_resume,
                                      send_vehicle_notify)

scheduler = AsyncIOScheduler()


def scheduler_jobs():
    # напоминание о заказе техники с "пн" по "чт"
    scheduler.add_job(
        send_vehicle_notify,
        'cron',
        day_of_week='mon-thu',
        hour=16,
        minute=0,
        timezone=const.TIME_ZONE
    )
    # напоминание о заказе техники в "пятницу"
    scheduler.add_job(
        send_vehicle_notify,
        'cron',
        day_of_week='fri',
        hour=11,
        minute=30,
        timezone=const.TIME_ZONE
    )
    # scheduler.add_job(
    #     send_vehicle_month_resume,
    #     'cron',
    #     day='1',
    #     hour=10,
    #     minute=0,
    #     timezone=const.TIME_ZONE
    # )
