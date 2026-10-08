from app.main import greet


def test_greet():
    assert greet("Sebastian") == "Hello, Sebastian!"
