import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from cryptography.fernet import Fernet
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

# carrega .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

if not all([USER, PASSWORD, HOST, PORT, DBNAME]):
    raise ValueError("Uma ou mais variáveis de conexão estão faltando no .env")

PASSWORD_ENCODED = quote_plus(PASSWORD)
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY not set in .env")

fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str

settings = Settings()
mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB]
