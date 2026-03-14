from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    open_router_api_key: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    open_router_api_key: Optional[str] = None  # mostra já descriptografada

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    password: Optional[str] = None
    open_router_api_key: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
