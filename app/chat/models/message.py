from pydantic import BaseModel

from app.genai.available_models import AvailableModels

class SendMessage(BaseModel):
    genai_model: AvailableModels 
    prompt: str

class Message(BaseModel):
    ...