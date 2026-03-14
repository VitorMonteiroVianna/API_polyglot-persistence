from abc import ABC

from app.genai.available_models import AvailableModels
from app.chat.messages import UserMessage, GenaiMessage


class IGenaiHander(ABC):
    def get_completions(self, user_message: UserMessage) -> GenaiMessage:
        raise NotImplementedError()

    def get_embedding(self, text: str, model: AvailableModels) -> list[float]:
        raise NotImplementedError()
