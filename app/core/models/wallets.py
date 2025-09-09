import uuid
from decimal import Decimal
from sqlalchemy import Uuid, Numeric, String, CheckConstraint, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, server_default=text("0"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="wallets")

    __table_args__ = (
        CheckConstraint("balance >= 0", name="wallet_balance_nonnegative"),
    )


class WalletOperation(Base):
    __tablename__ = "wallet_operations"

    wallet_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), index=True)
    operation_type: Mapped[str] = mapped_column(String(16), nullable=False)  # DEPOSIT / WITHDRAW
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False)
