from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from ...core.interfaces import UserRepository, ItemRepository
from ...user.model import User, CartItem
from ...item.model import Item


class SQLUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        return user

    def find_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_cart_items(self, user_id: UUID) -> List[CartItem]:
        return self.db.query(CartItem).filter(CartItem.user_id == user_id).all()


class SQLItemRepository(ItemRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        return item

    def get_all(self) -> List[Item]:
        return self.db.query(Item).all()

    def find_by_name(self, name: str) -> Optional[Item]:
        return self.db.query(Item).filter(Item.name == name).first()

    def find_by_id(self, id: UUID) -> Optional[Item]:
        return self.db.query(Item).filter(Item.id == id).first()
