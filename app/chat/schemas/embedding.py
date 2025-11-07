from pydantic import BaseModel, Field
from typing import List, Optional
from app.genai.available_models import AvailableModels

class EmbeddingPayload(BaseModel):
    text: str = Field(..., description="Texto que será convertido em embedding")
    metadata: Optional[dict] = Field(None, description="Metadados opcionais (ex: título, categoria)")
    model: AvailableModels = Field(default=AvailableModels.GPT_4_1_MINI, description="Modelo usado para gerar embeddings")

class EmbeddingResponse(BaseModel):
    id: str
    text: str
    vector: List[float]
    metadata: Optional[dict] = None
    dimension: int
