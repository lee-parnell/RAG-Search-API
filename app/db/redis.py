import redis.asyncio as redis  
from ..core.config import get_settings

setting = get_settings()

async def get_redis_client():
    return redis.from_url(setting.REDIS_URL, decode_responses=True)
