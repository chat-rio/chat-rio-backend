from fastapi import WebSocket
from datetime import datetime
from app.websocket.connection_manager import manager
from app.websocket.pubsub import publish_message
from app.core.jwt import verify_token
from app.db.mongo import db
from app.services.chat_service import get_message_collection

async def websocket_endpoint(websocket: WebSocket, user_id: str):
    token = websocket.query_params.get("token")
    if not token or not verify_token(token, user_id):
        await websocket.close()
        return
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event")
            to = data.get("to")
            content = data.get("content")

            if event == "message" and to and content:
                collection = get_message_collection(user_id, to)

                msg_doc = {
                    "sender_id": user_id,
                    "receiver_id": to,
                    "content": content,
                    "created_at": datetime.utcnow(),
                    "seen": None
                }
                await db[collection].insert_one(msg_doc)

                payload = {
                    "event": "message",
                    "from": user_id,
                    "to": to,
                    "content": content,
                    "created_at": msg_doc["created_at"].isoformat()
                }

                await publish_message(payload)
                await manager.send_personal_message(user_id, payload)

            elif event == "typing" and to:
                typing = data.get("typing", True)
                await publish_message({
                    "event": "typing",
                    "from": user_id,
                    "to": to,
                    "typing": typing
                })

            elif event == "seen" and to:
                collection = get_message_collection(user_id, to)

                now = datetime.utcnow()
                await db[collection].update_many(
                    {"sender_id": to, "receiver_id": user_id, "seen": None},
                    {"$set": {"seen": now}}
                )

                await publish_message({
                    "event": "seen",
                    "from": user_id,
                    "to": to,
                    "timestamp": now.isoformat()
                })

    except Exception as e:
        print(f"❌ WebSocket error for {user_id}: {e}")
    finally:
        await manager.disconnect(user_id)
