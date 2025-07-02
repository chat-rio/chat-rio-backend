from app.db.mongo import db
from app.schemas.user import UserCreate, UserInDB
from app.core.security import hash_password, verify_password
from bson import ObjectId

async def get_user_by_username(username: str):
    user = await db.users.find_one({"username": username})
    if user:
        user["id"] = str(user["_id"])
        return user
    return None

async def create_user(user: UserCreate):
    existing = await get_user_by_username(user.username)
    if existing:
        return None

    user_dict = {
        "username": user.username,
        "hashed_password": hash_password(user.password)
    }
    result = await db.users.insert_one(user_dict)
    return {
        "id": str(result.inserted_id),
        "username": user.username
    }

async def authenticate_user(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user
