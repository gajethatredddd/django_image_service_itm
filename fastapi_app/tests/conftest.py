import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)