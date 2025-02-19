from typing import Optional
from sqlalchemy.orm import Session
from ..infrastructure.sql.repositories import SQLUserRepository, SQLItemRepository
from .interfaces import UserRepository, ItemRepository


class Container:
    def __init__(self, testing: bool = False):
        self.testing = testing
        self.db: Optional[Session] = None
        self._user_repository: Optional[UserRepository] = None
        self._item_repository: Optional[ItemRepository] = None

    def set_db(self, db: Session) -> None:
        self.db = db
        if not self.testing:
            self._user_repository = SQLUserRepository(db)
            self._item_repository = SQLItemRepository(db)

    @property
    def user_repository(self) -> UserRepository:
        if self._user_repository is None:
            raise ValueError("Repository not initialized")
        return self._user_repository

    @user_repository.setter
    def user_repository(self, repo: UserRepository) -> None:
        self._user_repository = repo

    @property
    def item_repository(self) -> ItemRepository:
        if self._item_repository is None:
            raise ValueError("Repository not initialized")
        return self._item_repository

    @item_repository.setter
    def item_repository(self, repo: ItemRepository) -> None:
        self._item_repository = repo
