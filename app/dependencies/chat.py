from typing import Annotated

from fastapi import Depends

from app.chat.interfaces.repository.i_chat_repository import IChatRepository
from app.chat.interfaces.runners.i_embedding_runner import IEmbeddingRunner
from app.chat.interfaces.i_chat_service import IChatService
from app.users.auth import get_current_user
from app.users.models import User
from app.statup import statup


def get_chat_repository() -> IChatRepository:
    return statup.get_chat_repository()


def get_embedding_runner(
    current_user: Annotated[User, Depends(get_current_user)],
) -> IEmbeddingRunner:
    return statup.build_embedding_runner(current_user)


def get_chat_service(
    current_user: Annotated[User, Depends(get_current_user)],
) -> IChatService:
    return statup.build_chat_service(current_user)
