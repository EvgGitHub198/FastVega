from datetime import datetime
from typing import TypeVar
from sqlalchemy import TIMESTAMP, func, Column, Integer, Float, String, Boolean, LargeBinary, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    __abstarct__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, index=True, autoincrement=True)
    email = Column(String(225), nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    full_name = Column(String(225), nullable=False)
    is_active = Column(Boolean, default=False)

    UniqueConstraint("email", name="uq_user_email")


    def __repr__(self):
        return "<User {full_name!r}>".format(full_name=self.full_name)


ModelType = TypeVar("ModelType", bound=Base)

