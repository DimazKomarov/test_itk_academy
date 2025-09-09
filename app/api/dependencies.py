from typing import Annotated

from fastapi import Depends

from utils.unitofwork import UnitOfWork
from services.users import UsersService
from services.wallets import WalletsService
from services.operations import OperationsService


def get_users_service(uow: Annotated[UnitOfWork, Depends(UnitOfWork)]) -> UsersService:
    return UsersService(uow)


def get_wallets_service(uow: Annotated[UnitOfWork, Depends(UnitOfWork)]) -> WalletsService:
    return WalletsService(uow)


def get_operations_service(uow: Annotated[UnitOfWork, Depends(UnitOfWork)]) -> OperationsService:
    return OperationsService(uow)
