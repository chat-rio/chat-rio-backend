from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from app.deps import get_current_user
from app.db.mongo import db
from datetime import datetime
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING
from app.services.chat_service import get_message_collection
import re
from fastapi import Path
from app.websocket.connection_manager import manager

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

class SendMessage(BaseModel):
    to: str
    content: str

@router.post("/send")
async def send_message(
    payload: SendMessage,
    current_user: UserOut = Depends(get_current_user)
):
    msg = {
        "sender_id": current_user.id,
        "receiver_id": payload.to,
        "content": payload.content,
        "created_at": datetime.utcnow(),
        "seen": None
    }
    await db.messages.insert_one(msg)
    return {"success": True}


@router.get("/messages/{user_id}")
async def get_messages(user_id: str, current_user: UserOut = Depends(get_current_user)):
    collection = get_message_collection(current_user.id, user_id)
    cursor = db[collection].find({}).sort("created_at", 1)
    result = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        result.append(doc)
    return result

@router.get("/list")
async def get_chat_list(current_user: UserOut = Depends(get_current_user)):
    collections = await db.list_collection_names()
    user_id = current_user.id
    chat_partners = []
    for col in collections:
        if not col.startswith("messages_"):
            continue
        match = re.match(r"messages_(.+)_(.+)", col)
        if not match:
            continue
        user1, user2 = match.groups()
        if user_id not in [user1, user2]:
            continue
        partner_id = user2 if user1 == user_id else user1
        partner = await db.users.find_one({"_id": partner_id})
        if not partner:
            continue
        last_msg = await db[col].find_one(
            {},
            sort=[("created_at", DESCENDING)]
        )
        unread_count = await db[col].count_documents({
            "sender_id": partner_id,
            "receiver_id": user_id,
            "seen": None
        })
        chat_partners.append({
            "user_id": partner_id,
            "username": partner["username"],
            "last_message": last_msg["content"] if last_msg else "",
            "last_time": last_msg["created_at"].isoformat() if last_msg else "",
            "unread_count": unread_count
        })
    chat_partners.sort(key=lambda x: x["last_time"], reverse=True)
    return chat_partners


@router.post("/seen/{user_id}")
async def mark_messages_seen(
    user_id: str,
    current_user: UserOut = Depends(get_current_user)
):
    collection_name = get_message_collection(current_user.id, user_id)
    now = datetime.utcnow()
    result = await db[collection_name].update_many(
        {
            "sender_id": user_id,
            "receiver_id": current_user.id,
            "seen": None
        },
        {"$set": {"seen": now}}
    )
    await manager.send_personal_message(user_id, {
        "event": "seen",
        "from": current_user.id,
        "to": user_id,
        "timestamp": now.isoformat()
    })
    return {
        "success": True,
        "updated_count": result.modified_count
    }