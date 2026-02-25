import pytest
from flask import g, session
from flaskr.db import get_db

# Test register


def test_register(client, app):
    """
    Test register a new user
    Get should return with 200, error is a different code
    Post with data should create user (test in db) and redirect to login
    """
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert (
            get_db()
            .execute(
                "SELECT * FROM user WHERE username = 'a'",
            )
            .fetchone()
            is not None
        )


# pytest.mark.parametrize tells Pytest to run the same test function with different arguments.
@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    """Test register user end point, with expected result"""
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


# test login


def test_login(client, auth):
    """
    login Get returns form.
    auth logs a user (see conftest.py), should redirect to /
    Test session has user info
    """

    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"Incorrect username."),
        ("test", "a", b"Incorrect password."),
    ),
)
def test_login_validate_input(auth, username, password, message):
    """login wrong options"""
    response = auth.login(username, password)
    assert message in response.data


# Test logout


def test_logout(client, auth):
    """Test log out deletes session"""
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
