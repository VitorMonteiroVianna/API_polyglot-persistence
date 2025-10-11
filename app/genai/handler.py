from app.services.open_router import OpenRouterService

from app.users.models import User
from app.users import auth



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

    def get_completions(
            self, 
            message: str, 
            model: str = "gemini-2.5-flash", 
            max_tokens: int = 256, 
            temperature: float = 1.0
    ) -> dict:     # TODO: adicional uma BaseModel com o conteudo da resposta
        
        return self.open_router.generate_response(
            message = message,
            model= model,
            max_tokens= max_tokens,
            temperature= temperature,
        )
