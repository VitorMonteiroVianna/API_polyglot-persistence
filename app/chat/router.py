from typing import Annotated

from fastapi import APIRouter, Depends
from app.dependencies.chat import get_chat_repository

from app.users.auth import get_current_user
from app.users.models import User

from app.chat.chat import ChatService
from app.chat.model import SendMessagePayload
from app.chat.interfaces.repository.i_chat_repository import IChatRepository
from app.genai.handler import GenaiHander
from app.chat.runners.embedding import EmbeddingRunner

from app.chat.schemas.embedding import EmbeddingPayload, EmbeddingResponse

router = APIRouter()


@router.post("/chat/send")
async def send(
    payload: SendMessagePayload,
    repo: Annotated[IChatRepository, Depends(get_chat_repository)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    handler = GenaiHander(user=current_user)
    service = ChatService(repository=repo, handler=handler, user=current_user)
    return await service.send_message(user_id=str(current_user.id), payload=payload)

@router.post("/embedding", response_model=EmbeddingResponse)
def embedding(
    payload: EmbeddingPayload,
    current_user: Annotated[User, Depends(get_current_user)]
):
    runner = EmbeddingRunner(user=current_user)
    res = runner.run(payload)
    return res
