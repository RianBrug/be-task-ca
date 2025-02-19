from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from .container import Container
from ..database import SessionLocal

# Move the session creation to module level
db_session = SessionLocal()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create the Depends object at module level
db_dependency = Depends(get_db)


def get_container(db: Session = db_dependency) -> Container:
    container = Container()
    container.set_db(db)
    return container
