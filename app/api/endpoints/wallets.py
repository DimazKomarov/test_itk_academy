import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from api.schemas.wallet import OperationIn, WalletOut, OperationType, WalletCreate
from services.wallets import WalletsService
from api.dependencies import get_wallets_service, get_operations_service, get_users_service

from services.users import UsersService
from utils.security import get_current_token_payload
from services.operations import OperationsService

router = APIRouter(
    prefix="/wallet",
    tags=["Operations"],
)


@router.get("/wallets/{wallet_uuid}", response_model=WalletOut)
async def get_balance(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        users_service: Annotated[UsersService, Depends(get_users_service)],
        wallet_uuid: uuid.UUID,
        wallets_service: Annotated[WalletsService, Depends(get_wallets_service)],
) -> WalletOut:
    username = payload.get("sub")
    user = await users_service.get_user(username)
    if user:
        wallet = await wallets_service.get_wallet(wallet_uuid)
        if user.id != wallet.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this wallet"
            )
        elif wallet is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
        else:
            return {
                "id": str(wallet.id),
                "balance": wallet.balance,
                "user_id": wallet.user_id
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/wallets", response_model=WalletOut, status_code=201)
async def create_wallet(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        users_service: Annotated[UsersService, Depends(get_users_service)],
        wallets_service: Annotated[WalletsService, Depends(get_wallets_service)],
) -> WalletOut:
    username = payload.get("sub")
    user = await users_service.get_user(username)
    if user:
        wallet = await wallets_service.add_wallet(user_id=user.id)
        return wallet
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/wallets/{wallet_uuid}/operation", response_model=WalletOut, status_code=200)
async def operate(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        users_service: Annotated[UsersService, Depends(get_users_service)],
        wallet_uuid: uuid.UUID,
        operation: OperationIn,
        operations_service: Annotated[OperationsService, Depends(get_operations_service)],
        wallets_service: Annotated[WalletsService, Depends(get_wallets_service)],
) -> WalletOut:
    username = payload.get("sub")
    user = await users_service.get_user(username)
    if user:

        wallet = await wallets_service.get_wallet(wallet_uuid)
        if user.id != wallet.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this wallet"
            )

        if operation.operation_type == OperationType.DEPOSIT:
            wallet = await operations_service.deposit(wallet_uuid, operation.amount)
        elif operation.operation_type == OperationType.WITHDRAW:
            wallet = await operations_service.withdraw(wallet_uuid, operation.amount)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation type")
        return WalletOut(id=str(wallet.id), balance=wallet.balance, user_id=wallet.user_id)

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен!",
            headers={"WWW-Authenticate": "Bearer"},
        )