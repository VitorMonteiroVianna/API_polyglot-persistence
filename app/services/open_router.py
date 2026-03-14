import os
import requests

from app.genai.available_models import AvailableModels
from app.services.interfaces.i_open_router_service import IOpenRouterService

class OpenRouterService(IOpenRouterService):
    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("OPEN_ROUTER_KEY environment variable is not set.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_response(
        self,
        message: str,
        model: AvailableModels = AvailableModels.GEMINI_2_5_FLASH,
        max_tokens: int = 256,
        temperature: float = 1.0
    ) -> dict:
        completions_url = f"{self.BASE_URL}/chat/completions"

        model_id = model.capitalize()
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        response = requests.post(completions_url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def generate_embedding(
            self, text: str, model: AvailableModels
    ) -> list[float]:
        """Chama o endpoint de embeddings do OpenRouter."""
        response = requests.post(
            f"{self.BASE_URL}/embeddings",
            headers=self.headers,
            json={"model": model.value, "input": text},
        )
        response.raise_for_status()
        data = response.json()

        return data["data"][0]["embedding"]
