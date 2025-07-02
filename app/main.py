from fastapi import FastAPI
from app.api import routes_user, routes_chat
from app.config import settings
from app.websocket.events import websocket_endpoint
from fastapi.middleware.cors import CORSMiddleware
from app.core.redis import init_redis
import asyncio
from app.websocket.pubsub import redis_subscriber

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_api_websocket_route("/ws/{user_id}", websocket_endpoint)

@app.on_event("startup")
async def startup():
    await init_redis()
    asyncio.create_task(redis_subscriber())
# API
app.include_router(routes_user.router)
app.include_router(routes_chat.router)
@app.get("/")
async def root():
    return {"message": "Chat Rio backend is running"}