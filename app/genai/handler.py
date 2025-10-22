from typing import Dict

from app.services.open_router import OpenRouterService
from app.users.models import User
from app.users import auth
from app.genai.available_models import AvailableModels
from app.chat.models.message import CompletionTokenDetails, GenaiModelUsage, GenaiMessage

from app.shared import utils

class GenaiHander:
    def __init__(self, user: User):
        self.user= user
        self.open_router: OpenRouterService = self.start_open_router_service()
    
    def start_open_router_service(self):
        open_router_api_key = self.get_user_api_key()
        return OpenRouterService(api_key= open_router_api_key)
    
    def get_user_api_key(self):
        encrypted_key = self.user.open_router_api_key
        decrypted_key = auth.decrypt_api_key(token= encrypted_key)

        return decrypted_key

    def create_genai_message_from_open_router_res(
        self,
        open_router_res: Dict
    ) -> GenaiMessage:
        """
        Cria um objeto GenaiMessage a partir da resposta retornada pelo 
        OpenRouter.
        """
        message_id = utils.generate_hash_id()

        choice = open_router_res["choices"][0]
        message_data = choice["message"]

        usage_data = open_router_res.get("usage", {})

        completion_details_data = usage_data.get("completion_tokens_details")
        completion_details = None
        if completion_details_data:
            completion_details = CompletionTokenDetails(
                **completion_details_data
            )

        usage = GenaiModelUsage(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0),
            completion_tokens_details=completion_details
        )

        return GenaiMessage(
            message_id=message_id,
            genai_role=message_data.get("role", "assistant"),
            text=message_data.get("content", ""),
            genai_model=AvailableModels(open_router_res["model"]),
            usage=usage
        )

    def get_completions(
            self, 
            message: str, 
            model: AvailableModels = AvailableModels.GEMINI_2_5_FLASH, 
            max_tokens: int = 256, 
            temperature: float = 1.0
    ) -> GenaiMessage:
        
        open_router_res = self.open_router.generate_response(
            message = message,
            model= model,
            max_tokens= max_tokens,
            temperature= temperature,
        )
        genai_message = self.create_genai_message_from_open_router_res(
            open_router_res
        )

        return genai_message