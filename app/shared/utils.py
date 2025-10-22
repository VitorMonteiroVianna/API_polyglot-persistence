import uuid
import hashlib

def generate_hash_id() -> str:
    """
    Gera um hash_id único e curto baseado em UUID4.
    Retorna uma string hexadecimal de 16 caracteres.
    """
    unique_id = uuid.uuid4().hex 
    hash_id = hashlib.sha256(unique_id.encode()).hexdigest()[:20]
    return hash_id
