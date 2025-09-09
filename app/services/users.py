from fastapi import HTTPException, status

from utils.unitofwork import UnitOfWork
from utils.security import hash_password, validate_password
from api.schemas.user import UserOut


class UsersService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_user(self, user_data: dict) -> UserOut:
        async with self.uow:
            user_data["password"] = hash_password(user_data["password"])
            user = await self.uow.users.add_one(user_data)
            result = UserOut.model_validate(user)
            await self.uow.commit()
            return result

    async def get_user(self, username: str) -> UserOut | None:
        async with self.uow:
            user_from_db = await self.uow.users.find_one_or_none(username=username)
            if user_from_db:
                result = UserOut.model_validate(user_from_db)
                return result
            return None

    async def get_auth_user(self, username: str, password: str) -> UserOut:
        async with self.uow:
            user_from_db = await self.uow.users.find_one_or_none(username=username)

            if not user_from_db or not validate_password(password, user_from_db.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный логин или пароль!",
                )

            result = UserOut.model_validate(user_from_db)
            return result
