import web
import os
import pytest

@pytest.fixture
def app():
    os.environ["ACCESS_TOKEN"] = "1"
    return web.app
