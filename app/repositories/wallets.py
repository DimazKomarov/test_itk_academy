import uuid
from decimal import Decimal

from repositories.base import BaseRepository
from core.models.wallets import Wallet
from sqlalchemy import insert, select


class WalletRepository(BaseRepository):
    model = Wallet

    async def add_one(self, user_id: int) -> Wallet:
        stmt = insert(self.model).values(
            user_id=user_id,
            balance=Decimal("0.00")
        ).returning(self.model)
        res = await self.session.execute(stmt)
        wallet = res.scalar_one()
        return wallet

    async def get_for_update(self, wallet_id: uuid.UUID) -> Wallet | None:
        stmt = select(self.model).where(self.model.id == wallet_id).with_for_update()
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update_balance(self, wallet: Wallet, new_balance: Decimal):
        wallet.balance = new_balance
        self.session.add(wallet)
        await self.session.flush()
        return wallet