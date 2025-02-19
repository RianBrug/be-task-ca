from fastapi import HTTPException
from ..core.interfaces import ItemRepository
from .model import Item
from .schema import CreateItemRequest, CreateItemResponse, GetItemsResponse


class ItemService:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    def create_item(self, item: CreateItemRequest) -> CreateItemResponse:
        search_result = self.item_repository.find_by_name(item.name)
        if search_result is not None:
            raise HTTPException(
                status_code=409, detail="An item with this name already exists"
            )

        new_item = Item()  # type: ignore  # SQLAlchemy model initialization
        new_item.name = item.name
        new_item.description = item.description
        new_item.price = item.price
        new_item.quantity = item.quantity

        saved_item = self.item_repository.save(new_item)
        return self._model_to_schema(saved_item)

    def get_all(self) -> GetItemsResponse:
        item_list = self.item_repository.get_all()
        return GetItemsResponse(items=list(map(self._model_to_schema, item_list)))

    def _model_to_schema(self, item: Item) -> CreateItemResponse:
        return CreateItemResponse(
            id=item.id,
            name=str(item.name),
            description=str(item.description) if item.description else None,
            price=float(item.price),  # type: ignore  # SQLAlchemy Mapped type conversion
            quantity=int(item.quantity),  # type: ignore  # SQLAlchemy Mapped type conversion
        )
