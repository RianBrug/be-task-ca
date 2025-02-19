from typing import Dict, List, Optional
import uuid
from ...core.interfaces import UserRepository, ItemRepository
from ...user.model import User, CartItem
from ...item.model import Item


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: Dict[uuid.UUID, User] = {}
        self.cart_items: List[CartItem] = []

    def find_by_id(self, id: uuid.UUID) -> Optional[User]:
        user = self.users.get(id)
        if user:
            # Attach cart items to user
            user.cart_items = [item for item in self.cart_items if item.user_id == id]
        return user

    def find_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self.users.values() if u.email == email), None)

    def save(self, user: User) -> User:
        if user.id is None:
            user.id = uuid.uuid4()
        self.users[user.id] = user

        # Save cart items
        if user.cart_items:
            for item in user.cart_items:
                if item not in self.cart_items:
                    self.cart_items.append(item)

        return user

    def find_cart_items(self, user_id: uuid.UUID) -> List[CartItem]:
        return [item for item in self.cart_items if item.user_id == user_id]


class InMemoryItemRepository(ItemRepository):
    def __init__(self):
        self.items: Dict[uuid.UUID, Item] = {}

    def find_by_id(self, id: uuid.UUID) -> Optional[Item]:
        return self.items.get(id)

    def find_by_name(self, name: str) -> Optional[Item]:
        return next((i for i in self.items.values() if i.name == name), None)

    def save(self, item: Item) -> Item:
        if item.id is None:
            item.id = uuid.uuid4()
        self.items[item.id] = item
        return item

    def get_all(self) -> List[Item]:
        return list(self.items.values())
