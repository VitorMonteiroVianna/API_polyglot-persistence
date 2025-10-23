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