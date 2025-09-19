from fastapi import APIRouter, Depends
from app.users.auth import get_current_user
from app.users.models import User

router = APIRouter()

@router.get("/test")
def test_chat(current_user: User = Depends(get_current_user)):
    return {"message": f"Olá, {current_user.email}! Você acessou a rota protegida."}
