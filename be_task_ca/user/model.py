from dataclasses import dataclass
from typing import List
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from be_task_ca.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class CartItem(Base):
    __tablename__ = "cart_items"

    quantity: Mapped[int]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, index=True
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("items.id"), primary_key=True
    )


@dataclass
class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    shipping_address: Mapped[str | None] = mapped_column(default=None)
    cart_items: Mapped[List["CartItem"]] = relationship()
