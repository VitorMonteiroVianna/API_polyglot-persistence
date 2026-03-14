import os
import certifi
from dotenv import load_dotenv
from urllib.parse import quote_plus
from cryptography.fernet import Fernet
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict

# carrega .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    USER = os.getenv("DB_USER") or os.getenv("USER")
    PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("PASSWORD")
    HOST = os.getenv("DB_HOST") or os.getenv("HOST")
    PORT = os.getenv("DB_PORT") or os.getenv("PORT")
    DBNAME = os.getenv("DB_NAME") or os.getenv("DBNAME")

    if all([USER, PASSWORD, HOST, PORT, DBNAME]):
        assert USER is not None
        assert PASSWORD is not None
        assert HOST is not None
        assert PORT is not None
        assert DBNAME is not None
        PASSWORD_ENCODED = quote_plus(PASSWORD)
        DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    else:
        DATABASE_URL = "sqlite:///./app.db"

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key().decode()

fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "chat_db"
    MONGO_CONVERSATIONS_COLLECTION: str = "chat_conversations"
    MONGO_MESSAGES_COLLECTION: str = "chat_messages"
    MONGO_TLS_CA_FILE: str = certifi.where()
    MONGO_ALLOW_INVALID_CERTS: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
mongo_client_kwargs = {}

if settings.MONGO_URI.startswith("mongodb+srv://"):
    mongo_client_kwargs["tlsCAFile"] = settings.MONGO_TLS_CA_FILE

if settings.MONGO_ALLOW_INVALID_CERTS:
    mongo_client_kwargs["tlsAllowInvalidCertificates"] = True

mongo_client = AsyncIOMotorClient(settings.MONGO_URI, **mongo_client_kwargs)
mongo_db = mongo_client[settings.MONGO_DB]
