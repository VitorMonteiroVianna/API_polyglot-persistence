from functools import lru_cache

from app.chat.repository import MongoChatRepository
from app.core.config import mongo_db


@lru_cache
def get_chat_repository() -> MongoChatRepository:
    return MongoChatRepository(mongo_db)