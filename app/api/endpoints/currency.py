from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.currency import CurrencyPair
from services.external import ExternalService

from utils.security import get_current_token_payload

from api.dependencies import get_users_service
from services.users import UsersService


router = APIRouter(
    prefix="/currency",
    tags=["Currency transactions"],
)


@router.get("/list")
async def get_list_of_currencies(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        users_service: Annotated[UsersService, Depends(get_users_service)],
) -> dict:
    username = payload.get("sub")
    user = await users_service.get_user(username)
    if user:
        return await ExternalService.get_list_of_currencies()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/exchange")
async def convert_currencies(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        users_service: Annotated[UsersService, Depends(get_users_service)],
        currency_pair: CurrencyPair,
) -> dict:
    username = payload.get("sub")
    user = await users_service.get_user(username)
    if user:
        return await ExternalService.convert_currencies(currency_pair.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен!",
            headers={"WWW-Authenticate": "Bearer"},
        )
