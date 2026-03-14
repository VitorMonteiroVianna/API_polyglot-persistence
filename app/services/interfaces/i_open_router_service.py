from abc import ABC

from app.genai.available_models import AvailableModels


class IOpenRouterService(ABC):
    def generate_response(
        self,
        message: str,
        model: AvailableModels = AvailableModels.GEMINI_2_5_FLASH,
        max_tokens: int = 256,
        temperature: float = 1.0,
    ) -> dict:
        raise NotImplementedError()

    def generate_embedding(self, text: str, model: AvailableModels) -> list[float]:
        raise NotImplementedError()
