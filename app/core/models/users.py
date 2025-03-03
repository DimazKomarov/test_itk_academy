from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'
