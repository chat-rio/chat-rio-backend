import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chat-Rio"
    API_V1_STR: str = "/api/v1"
    # JWT
    SECRET_KEY: str = "ngaybuonlangayanhmatem"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "fastchat"
    # Redis
    REDIS_URL: str = "redis://192.168.100.39:6379"

settings = Settings()