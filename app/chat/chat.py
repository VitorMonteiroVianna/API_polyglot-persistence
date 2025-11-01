from typing import List, Optional, Union

from shared import utils

from app.chat.messages import GenaiMessage, UserMessage

from app.chat.tokens import GenaiModelUsage

from app.genai.available_models import AvailableModels


class Chat:
    """
    Representa uma sessão de conversa (chat) com um modelo de IA.
    Armazena mensagens e estatísticas agregadas (tokens, contagem, etc.)
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.chat_id: str
        self.messages: List[Union[GenaiMessage, UserMessage]] = []
        self.tokens_used: GenaiModelUsage
        self.models_used: List[AvailableModels]


    def get_chat_by_id(self, chat_id: str):
        #TODO: resgatar o chat usando o banco
        # - nao usar o banco diretamente, e sim por um handler
        ...
        
    def start_chat(self, chat_id: str | None):
        if chat_id:
            self.get_chat_by_id()
            
        



    def create_chat_id(self) -> str:
        return utils.generate_hash_id()

    def add_message(self, message: Union[GenaiMessage, UserMessage]):
        self.messages.append(message)
