import redis
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

# Create the client
client = RedisStorage(redis)
storage = RedisStorage.from_url(
    'redis://localhost:6379/1',
    key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
)
