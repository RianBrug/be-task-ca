from fastapi import APIRouter, Depends
from ..core.dependencies import get_container
from .schema import CreateItemRequest, CreateItemResponse
from .usecases import ItemService

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


def get_item_service(container=Depends(get_container)) -> ItemService:
    return ItemService(container.item_repository)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest, service: ItemService = Depends(get_item_service)
) -> CreateItemResponse:
    return service.create_item(item)


@item_router.get("/")
async def get_items(service: ItemService = Depends(get_item_service)):
    return service.get_all()
