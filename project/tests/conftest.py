import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.main import create_application


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    register_tortoise(
        app,
        db_url=os.getenv("DATABASE_TEST_URL"),
        modules={"models": ["app.entity.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client
