from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Message(BaseModel):
    id: Optional[str] = Field(alias="_id")
    sender_id: str
    receiver_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    seen: Optional[datetime] = None
