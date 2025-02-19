from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import logging

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:example@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_db_schema():
    Base.metadata.create_all(bind=engine)
