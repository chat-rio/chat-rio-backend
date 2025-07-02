import asyncio
import json
import app.core.redis as redis_core
from app.websocket.connection_manager import manager

CHANNEL_NAME = "chat_messages"

async def publish_message(message: dict):
    print("🚀 Publishing message:", message)  # 👈 thêm dòng này
    if redis_core.redis is None:
        print("❌ Redis is not initialized")
        return
    await redis_core.redis.publish(CHANNEL_NAME, json.dumps(message))

async def redis_subscriber():
    pubsub = redis_core.redis.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)
    print("✅ Subscribed to Redis channel:", CHANNEL_NAME)

    async for message in pubsub.listen():
        print("🔔 Redis received:", message)  # 👈 thêm dòng này

        if message["type"] == "message":
            data = json.loads(message["data"])
            print("📨 Redis parsed data:", data)  # 👈 thêm dòng này
            to_user = data.get("to")
            if to_user:
                await manager.send_personal_message(to_user, data)
