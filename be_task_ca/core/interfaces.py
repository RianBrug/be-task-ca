from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..user.model import User, CartItem
from ..item.model import Item


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def find_cart_items(self, user_id: UUID) -> List[CartItem]:
        pass


class ItemRepository(ABC):
    @abstractmethod
    def save(self, item: Item) -> Item:
        pass

    @abstractmethod
    def get_all(self) -> List[Item]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Item]:
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> Optional[Item]:
        pass
