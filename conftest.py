import os
import pytest
import web

@pytest.fixture
def app():
    os.environ["ACCESS_TOKEN"] = "1"
    app = web.create_app(sqlite_path='sqlite:///test_intent.db')
    #app = create_app()
    import dbms.create_db
    return app
