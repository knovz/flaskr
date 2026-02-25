# Pytest uses fixtures by matching their function names
# with the names of arguments in the test functions.
# For example, the test_hello function takes a client argument.
# Pytest matches that with the client fixture function,
# calls it, and passes the returned value to the test function.

# There’s not much to test about the factory itself.
# Most of the code will be executed for each test already,
# so if something fails the other tests will notice.
# The only behavior that can change is passing test config.
# If config is not passed, there should be some default configuration,
# otherwise the configuration should be overridden.

from flaskr import create_app


def test_config():
    """
    If config is not passed, there should be some default configuration,
    otherwise the configuration should be overridden.
    """
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    """Test example /Hello route"""
    response = client.get("/hello")
    assert response.data == b"Hello, World of Flask!"
