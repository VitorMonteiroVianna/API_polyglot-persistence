from typing import Annotated

from fastapi import Depends

from app.users.auth import get_current_user
from app.users.models import User
from app.services.interfaces.i_open_router_service import IOpenRouterService
from app.genai.interfaces.i_genai_hander import IGenaiHander
from app.statup import statup


def get_open_router_service(
    current_user: Annotated[User, Depends(get_current_user)],
) -> IOpenRouterService:
    return statup.build_open_router_service(current_user)


def get_genai_handler(
    current_user: Annotated[User, Depends(get_current_user)],
) -> IGenaiHander:
    return statup.build_genai_handler(current_user)
