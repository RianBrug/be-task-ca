import hashlib
from fastapi import HTTPException
from ..core.interfaces import UserRepository, ItemRepository
from .model import CartItem, User
from .schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)
from uuid import UUID


class UserService:
    def __init__(
        self, user_repository: UserRepository, item_repository: ItemRepository
    ):
        self.user_repository = user_repository
        self.item_repository = item_repository

    def create_user(self, create_user: CreateUserRequest) -> CreateUserResponse:
        search_result = self.user_repository.find_by_email(create_user.email)
        if search_result is not None:
            raise HTTPException(
                status_code=409, detail="An user with this email address already exists"
            )

        new_user = User()  # type: ignore  # SQLAlchemy model initialization
        new_user.first_name = create_user.first_name
        new_user.last_name = create_user.last_name
        new_user.email = create_user.email
        new_user.hashed_password = hashlib.sha512(
            create_user.password.encode("UTF-8")
        ).hexdigest()
        new_user.shipping_address = create_user.shipping_address

        saved_user = self.user_repository.save(new_user)
        return CreateUserResponse(
            id=saved_user.id,
            first_name=str(saved_user.first_name),
            last_name=str(saved_user.last_name),
            email=str(saved_user.email),
            shipping_address=str(saved_user.shipping_address)
            if saved_user.shipping_address
            else None,
        )

    def add_item_to_cart(
        self, user_id: UUID, cart_item: AddToCartRequest
    ) -> AddToCartResponse:
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User does not exist")

        item = self.item_repository.find_by_id(cart_item.item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item does not exist")
        if item.quantity < cart_item.quantity:
            raise HTTPException(status_code=409, detail="Not enough items in stock")

        item_ids = [o.item_id for o in user.cart_items]
        if cart_item.item_id in item_ids:
            raise HTTPException(status_code=409, detail="Item already in cart")

        new_cart_item = CartItem()  # type: ignore  # SQLAlchemy model initialization
        new_cart_item.user_id = user.id
        new_cart_item.item_id = cart_item.item_id
        new_cart_item.quantity = cart_item.quantity

        user.cart_items.append(new_cart_item)
        self.user_repository.save(user)

        return self.list_items_in_cart(user.id)

    def list_items_in_cart(self, user_id) -> AddToCartResponse:
        cart_items = self.user_repository.find_cart_items(user_id)
        return AddToCartResponse(items=list(map(self._cart_item_to_schema, cart_items)))

    def _cart_item_to_schema(self, model: CartItem) -> AddToCartRequest:
        return AddToCartRequest(
            item_id=model.item_id,
            quantity=int(model.quantity),  # type: ignore  # SQLAlchemy Mapped type conversion
        )
