from pydantic import BaseModel
from typing import Optional

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