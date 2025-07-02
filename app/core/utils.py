from datetime import datetime
from typing import Optional
import uuid


def get_timestamp_now() -> str:
    return datetime.utcnow().isoformat()


def generate_uuid() -> str:
    return str(uuid.uuid4())


def safe_get(d: dict, key: str, default=None):
    return d[key] if key in d else default


def truncate(text: str, max_length: int = 100) -> str:
    return text if len(text) <= max_length else text[:max_length] + "..."
