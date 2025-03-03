from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form

from api.schemas.user import UserIn
from services.users import UsersService
from api.dependencies import get_users_service

from utils.security import encode_jwt


router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: Annotated[UserIn, Form()],
        users_service: Annotated[UsersService, Depends(get_users_service)]
) -> dict:
    user = await users_service.get_user(user_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует!",
        )
    else:
        result = await users_service.add_user(user_data.model_dump())
        return {
            "message": "Вы успешно зарегистрированы!",
            "user_id": result.id,
        }


@router.post("/login")
async def login(
        user_data: Annotated[UserIn, Form()],
        users_service: Annotated[UsersService, Depends(get_users_service)],
) -> dict:
    user = await users_service.get_auth_user(
        user_data.username,
        user_data.password,
    )
    jwt_payload = {"sub": user.username}
    access_token = encode_jwt(jwt_payload)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
