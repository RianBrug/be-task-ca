from uuid import UUID
from fastapi import APIRouter, Depends
from ..core.dependencies import get_container
from .schema import AddToCartRequest, CreateUserRequest
from .usecases import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


def get_user_service(container=Depends(get_container)) -> UserService:
    return UserService(container.user_repository, container.item_repository)


@user_router.post("/")
async def post_customer(
    user: CreateUserRequest, service: UserService = Depends(get_user_service)
):
    return service.create_user(user)


@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID,
    cart_item: AddToCartRequest,
    service: UserService = Depends(get_user_service),
):
    return service.add_item_to_cart(user_id, cart_item)


@user_router.get("/{user_id}/cart")
async def get_cart(user_id: UUID, service: UserService = Depends(get_user_service)):
    return service.list_items_in_cart(user_id)
