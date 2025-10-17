from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.mongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram.fsm.storage.base import DefaultKeyBuilder

from config.telegram_config import TELEGRAM_TOKEN

mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")

storage = MongoStorage(
    client=mongo_client,
    db_name="tehnika_bot_db",
    collection_name="states",
    key_builder=DefaultKeyBuilder(with_destiny=True),
)

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)
