import uuid

from utils.unitofwork import UnitOfWork
from api.schemas.wallet import WalletOut


class WalletsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_wallet(self, wallet_uuid: uuid.UUID) -> WalletOut | None:
        async with self.uow:
            wallet_from_db = await self.uow.wallets.find_one_or_none(id=wallet_uuid)
            if wallet_from_db:
                result = WalletOut(
                    id=str(wallet_from_db.id),
                    balance=wallet_from_db.balance,
                    user_id=wallet_from_db.user_id
                )
                return result
            return None

    async def add_wallet(self, user_id: int) -> WalletOut:
        async with self.uow:
            wallet = await self.uow.wallets.add_one(user_id)
            await self.uow.commit()
            return WalletOut(id=str(wallet.id), balance=wallet.balance, user_id=wallet.user_id)
