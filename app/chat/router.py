from fastapi import APIRouter, Depends
from app.users.auth import get_current_user
from app.users.models import User

from app.chat.runners.message import MessageRunner

router = APIRouter()


@router.post("/message")
def send(current_user: User = Depends(get_current_user)):

    runner = MessageRunner(user= current_user)
    res = runner.run()
    
    return res