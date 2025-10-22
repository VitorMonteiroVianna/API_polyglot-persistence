from pydantic import BaseModel
from typing import Optional

from app.genai.available_models import AvailableModels

class SendMessage(BaseModel):
    """
    Classe de usada como Model de body para o request na /chat/message
    """
    genai_model: AvailableModels 
    prompt: str


class CompletionTokenDetails(BaseModel):
    """
    Sub classe usada para dar informações adicionais sobre o consumo de
    um modelo, baseada no retorno do OpenRouter
    """
    reasoning_tokens: Optional[int] = 0
    image_tokens: Optional[int] = 0

class GenaiModelUsage(BaseModel):
    """
    Sub classe usada para dar informações gerais sobre o consumo de um 
    modelo, baseada no retorno do OpenRouter
    """
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    completion_tokens_details: Optional[CompletionTokenDetails] = None

class GenaiMessage(BaseModel):
    """
    Classe usada para armezenar as informações de uma interação com 
    modelos de LLM
    """
    message_id: str
    genai_role: str
    text: str
    genai_model: AvailableModels
    usage: GenaiModelUsage
