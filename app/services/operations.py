import uuid
from decimal import Decimal

from fastapi import HTTPException, status

from utils.unitofwork import UnitOfWork
from api.schemas.wallet import WalletOut


class OperationsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def deposit(self, wallet_id: uuid.UUID, amount: Decimal) -> WalletOut:
        async with self.uow:
            wallet = await self.uow.wallets.get_for_update(wallet_id)
            if wallet is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

            new_balance = (wallet.balance or Decimal("0.00")) + amount
            await self.uow.wallets.update_balance(wallet, new_balance)
            await self.uow.commit()
            return WalletOut(id=str(wallet.id), balance=wallet.balance, user_id=wallet.user_id)

    async def withdraw(self, wallet_id: uuid.UUID, amount: Decimal) -> WalletOut:
        async with self.uow:
            wallet = await self.uow.wallets.get_for_update(wallet_id)
            if wallet is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

            if wallet.balance < amount:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Insufficient funds in wallet {wallet.id}",
                )

            new_balance = wallet.balance - amount
            await self.uow.wallets.update_balance(wallet, new_balance)
            await self.uow.commit()
            return WalletOut(id=str(wallet.id), balance=wallet.balance, user_id=wallet.user_id)
