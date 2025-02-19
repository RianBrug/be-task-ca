import pytest
from fastapi.testclient import TestClient
from be_task_ca.app import app
from be_task_ca.core.container import Container
from be_task_ca.core.dependencies import get_container
from be_task_ca.infrastructure.memory.repositories import InMemoryUserRepository, InMemoryItemRepository

@pytest.fixture
def test_container():
    container = Container(testing=True)
    container.user_repository = InMemoryUserRepository()
    container.item_repository = InMemoryItemRepository()
    return container

@pytest.fixture
def client(test_container):
    def get_test_container():
        return test_container
    
    app.dependency_overrides[get_container] = get_test_container
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear() 