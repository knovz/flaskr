import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """To create the app in testing mode"""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """client to run tests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """to run the cli methods"""
    return app.test_cli_runner()


# For most of the views, a user needs to be logged in.
# We can make a POST request to the login view with the client.
# Rather than writing that out every time, we can write a class with methods to do that,
# and use a fixture to pass it the client for each test.
class AuthActions(object):
    """The test user is included in the test data. We define login and logout."""

    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        """login as test"""
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        """logout"""
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    """With this we can call auth.login and auth.logout in a test"""
    return AuthActions(client)
