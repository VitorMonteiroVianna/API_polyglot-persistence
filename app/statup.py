from functools import lru_cache

from app.chat.chat import ChatService
from app.chat.interfaces.i_chat_service import IChatService
from app.chat.interfaces.repository.i_chat_repository import IChatRepository
from app.chat.interfaces.runners.i_embedding_runner import IEmbeddingRunner
from app.chat.repository import MongoChatRepository
from app.chat.runners.embedding import EmbeddingRunner
from app.core.config import mongo_db
from app.genai.handler import GenaiHander
from app.genai.interfaces.i_genai_hander import IGenaiHander
from app.services.interfaces.i_open_router_service import IOpenRouterService
from app.services.open_router import OpenRouterService
from app.users import auth
from app.users.models import User


class Statup:
    @lru_cache
    def get_chat_repository(self) -> IChatRepository:
        return MongoChatRepository(mongo_db)

    def build_open_router_service(self, user: User) -> IOpenRouterService:
        encrypted_key = user.open_router_api_key
        encrypted_key_str = str(encrypted_key) if encrypted_key is not None else ""

        if not encrypted_key_str or encrypted_key_str == "None":
            raise ValueError("Usuário não possui open_router_api_key configurada")

        decrypted_key = auth.decrypt_api_key(token=encrypted_key_str)
        return OpenRouterService(api_key=decrypted_key)

    def build_genai_handler(self, user: User) -> IGenaiHander:
        open_router_service = self.build_open_router_service(user)
        return GenaiHander(open_router_service=open_router_service)

    def build_embedding_runner(self, user: User) -> IEmbeddingRunner:
        genai_handler = self.build_genai_handler(user)
        return EmbeddingRunner(user=user, genai_handler=genai_handler)

    def build_chat_service(self, user: User) -> IChatService:
        repository = self.get_chat_repository()
        genai_handler = self.build_genai_handler(user)
        embedding_runner = self.build_embedding_runner(user)
        return ChatService(
            repository=repository,
            handler=genai_handler,
            embedding_runner=embedding_runner,
        )


statup = Statup()
