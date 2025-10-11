from app.users.models import User
from app.users import auth


def get_decrypted_api_key(user: User) -> str:
    encrypted_api_key = user.open_router_api_key
    if not encrypted_api_key:
        return ValueError("O usuario não possui APIKey cadastrada")
    
    decrypeted_api_key = auth.decrypt_api_key(token= encrypted_api_key)
    
    return decrypeted_api_key