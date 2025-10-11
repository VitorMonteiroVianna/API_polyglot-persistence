from fastapi import FastAPI
import uvicorn

from app.users import router as users_router
from app.chat import router as chat_router
from app.users.models import Base, engine

# cria tabelas no banco (apenas dev; em produção use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI JWT Example")

app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(chat_router.router, prefix="/chat", tags=["chat"])

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )
