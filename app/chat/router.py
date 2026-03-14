from typing import Annotated

from fastapi import APIRouter, Depends
from app.dependencies.chat import get_chat_service, get_embedding_runner

from app.users.auth import get_current_user
from app.users.models import User

from app.chat.interfaces.i_chat_service import IChatService
from app.chat.model import SendMessagePayload
from app.chat.interfaces.runners.i_embedding_runner import IEmbeddingRunner

from app.chat.schemas.embedding import EmbeddingPayload, EmbeddingResponse

router = APIRouter()


@router.post("/chat/send")
async def send(
    payload: SendMessagePayload,
    service: Annotated[IChatService, Depends(get_chat_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await service.send_message(user_id=str(current_user.id), payload=payload)

@router.post("/embedding", response_model=EmbeddingResponse)
def embedding(
    payload: EmbeddingPayload,
    runner: Annotated[IEmbeddingRunner, Depends(get_embedding_runner)],
):
    res = runner.run(payload)
    return res
