from typing import Annotated
from pydantic import BaseModel, Field, field_validator

from app.genai.available_models import AvailableModels

class SendMessagePayload(BaseModel):
    """
    Classe de usada como Model de body para o request na /chat/message
    """
    chat_id: str | None
    genai_model: AvailableModels 
    prompt: str
    max_tokens: int
    temperature: Annotated[float, Field(ge=0.0, le=1.0)]

    @field_validator("temperature", mode="before")
    @classmethod
    def rount_temperature(cls, v):
        """
        Metodo para arredondar a temperatura para somente uma casa apos 
        decimal
        """
        return round(float(v), 1)