from typing import Annotated

from fastapi import Depends

from utils.unitofwork import UnitOfWork
from services.users import UsersService


def get_users_service(uow: Annotated[UnitOfWork, Depends(UnitOfWork)]) -> UsersService:
    return UsersService(uow)
