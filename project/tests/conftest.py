import os
from typing import Iterator
import asyncio

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import finalizer, initializer

from app.main import create_application


@pytest.fixture(scope="module")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def client(event_loop: asyncio.BaseEventLoop) -> Iterator[TestClient]:
    app = create_application()
    register_tortoise(
        app,
        db_url=os.getenv("DATABASE_TEST_URL"),
        modules={"models": ["app.entity.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    initializer(
        ["app.entity.models"],
        db_url=os.getenv("DATABASE_TEST_URL"),
        app_label="models",
        loop=event_loop,
    )
    with TestClient(app) as test_client:
        yield test_client
    finalizer()
