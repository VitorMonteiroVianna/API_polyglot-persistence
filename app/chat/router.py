from fastapi import APIRouter, Depends

from app.users.auth import get_current_user
from app.users.models import User

from app.chat.model import SendMessagePayload

from app.chat.runners.message import ChatRunner
from app.chat.runners.embedding import EmbeddingRunner

from app.chat.schemas.embedding import EmbeddingPayload, EmbeddingResponse

router = APIRouter()


@router.post("/message")
def send(
    payload: SendMessagePayload,
    current_user: User = Depends(get_current_user)
):
    runner = ChatRunner(user= current_user)
    res = runner.run(payload)
    return res

@router.post("/embedding", response_model=EmbeddingResponse)
def embedding(
    payload: EmbeddingPayload,
    current_user: User = Depends(get_current_user)
):
    runner = EmbeddingRunner(user=current_user)
    res = runner.run(payload)
    return res