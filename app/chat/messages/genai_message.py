from dataclasses import dataclass

from app.chat.messages.message import Message
from app.chat.tokens import GenaiModelUsage


@dataclass
class GenaiMessage(Message):
    """
    Classe usada para armazenar uma mensagem que retornada pelo modelo
    de Gen AI. 
    """
    user_message_id: str
    genai_role: str
    genai_usage: GenaiModelUsage

    def as_dict(self) -> dict:
        data = super().as_dict()
        if isinstance(self.genai_usage, GenaiModelUsage):
            data["genai_usage"] = self.genai_usage.model_dump()
        return data