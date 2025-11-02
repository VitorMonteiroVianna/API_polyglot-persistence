from fastapi import APIRouter, Depends
from app.dependencies.chat import get_chat_repository

from app.users.auth import get_current_user
from app.users.models import User

from app.chat.model import SendMessagePayload
from app.chat.repository import ChatRepository

from app.chat.runners.message import ChatRunner

router = APIRouter()


@router.post("/chat/send")
async def send(
    payload: SendMessagePayload,
    repo: ChatRepository = Depends(get_chat_repository),
    current_user: User = Depends(get_current_user),
):
    runner = ChatRunner(user= current_user)
    res = runner.run(payload)
    return res