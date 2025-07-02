def get_message_collection(user1: str, user2: str) -> str:
    sorted_ids = sorted([user1, user2])
    return f"messages_{sorted_ids[0]}_{sorted_ids[1]}"