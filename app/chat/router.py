from fastapi import APIRouter, Depends
from app.dependencies.chat import get_chat_repository

from app.users.auth import get_current_user
from app.users.models import User

from app.chat.chat import ChatService
from app.chat.model import SendMessagePayload
from app.chat.repository import ChatRepository
from app.genai.handler import GenaiHander

router = APIRouter()


@router.post("/chat/send")
async def send(
    payload: SendMessagePayload,
    repo: ChatRepository = Depends(get_chat_repository),
    current_user: User = Depends(get_current_user),
):
    handler = GenaiHander(user=current_user)
    service = ChatService(repository=repo, handler=handler)
    return await service.send_message(user_id=str(current_user.id), payload=payload)