import os
import pytest

@pytest.fixture
def app():
    os.environ["ACCESS_TOKEN"] = "1"
    import web
    app = web.create_app(sqlite_path='sqlite:///test_intent.db')
    #app = create_app()
    import dbms.create_db
    return app
