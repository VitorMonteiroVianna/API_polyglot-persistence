from pydantic import BaseModel

from app.genai.available_models import AvailableModels

class SendMessage(BaseModel):
    """
    Classe de usada como Model de body para o request na /chat/message
    """
    genai_model: AvailableModels 
    prompt: str
