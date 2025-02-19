from ...database import Base, engine

# These imports are needed to register the models with SQLAlchemy
# even though they appear unused to the linter
import be_task_ca.user.model  # noqa: F401
import be_task_ca.item.model  # noqa: F401


def create_db_schema():
    Base.metadata.create_all(bind=engine)
