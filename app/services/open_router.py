import os
import requests

class OpenRouterService:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    PREDEFINED_MODELS = {
        "gemini-2.5-flash": "google/gemini-2.5-flash",
        # TODO: adicionar os modelos aqui 
    }

    def __init__(self):
        self.api_key = os.getenv("OPEN_ROUTER_KEY")
        if not self.api_key:
            raise ValueError("OPEN_ROUTER_KEY environment variable is not set.")

    def select_model(self, model_name: str) -> str:
        model = self.PREDEFINED_MODELS.get(model_name)
        if not model:
            raise ValueError(f"Model '{model_name}' not found.")
        return model

    def generate_response(
        self, 
        message: str, 
        model: str = "gemini-2.5-flash", 
        max_tokens: int = 256, 
        temperature: float = 1.0
    ) -> dict:
        model_id = self.select_model(model)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        response = requests.post(self.BASE_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()