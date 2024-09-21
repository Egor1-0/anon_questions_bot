from datetime import datetime, timezone

from sqlalchemy import String, BigInteger, Boolean, DATETIME, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    self_reffer_id: Mapped[str] = mapped_column(String, nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean,default=True)
    when_reg: Mapped[datetime] = mapped_column(DATETIME, server_default=func.now())


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger)
    from_user_id: Mapped[int] = mapped_column(BigInteger)
    original_message: Mapped[int] = mapped_column(BigInteger)
    when_reg: Mapped[datetime] = mapped_column(DATETIME, server_default=func.now())