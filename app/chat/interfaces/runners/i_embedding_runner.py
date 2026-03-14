from abc import ABC

from app.genai.available_models import AvailableModels
from app.chat.schemas.embedding import EmbeddingPayload, EmbeddingResponse


class IEmbeddingRunner(ABC):
    def enrich_prompt(
        self,
        prompt: str,
        model: AvailableModels = AvailableModels.OPENAI_EMBEDDING_3_SMALL,
        top_k: int = 3,
    ) -> str:
        raise NotImplementedError()

    def run(self, payload: EmbeddingPayload) -> EmbeddingResponse:
        raise NotImplementedError()
