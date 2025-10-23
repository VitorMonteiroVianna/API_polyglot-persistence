from dataclasses import dataclass

from app.chat.messages.message import Message

from app.genai.available_models import AvailableModels


@dataclass
class UserMessage(Message):
    """
    Classe usada para armazenar os dados de uma mensagem enviada pelo
    usuario para Gen Ai
    """
    max_tokens: int
    temperature: float
