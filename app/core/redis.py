from redis.asyncio import Redis
from app.config import settings

redis: Redis | None = None

async def init_redis():
    global redis
    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    await redis.ping()
    print("✅ Redis connected")