import pytest

from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


def test_register_success(db):
    service = AuthService(db)

    request = RegisterRequest(
        full_name="Mohamed",
        email="mohamed@test.com",
        password="Password123",
    )

    user = service.register(request)

    assert user.id is not None
    assert user.email == request.email
    assert user.full_name == request.full_name

    # Ensure password wasn't stored as plain text
    assert user.hashed_password != request.password


def test_register_duplicate_email(db):
    service = AuthService(db)

    request = RegisterRequest(
        full_name="Mohamed",
        email="mohamed@test.com",
        password="Password123",
    )

    service.register(request)

    with pytest.raises(ValueError):
        service.register(request)


def test_login_success(db):
    service = AuthService(db)

    register_request = RegisterRequest(
        full_name="Mohamed",
        email="mohamed@test.com",
        password="Password123",
    )

    service.register(register_request)

    login_request = LoginRequest(
        email="mohamed@test.com",
        password="Password123",
    )

    token = service.login(login_request)

    assert isinstance(token, str)


def test_login_wrong_password(db):
    service = AuthService(db)

    service.register(
        RegisterRequest(
            full_name="Mohamed",
            email="mohamed@test.com",
            password="Password123",
        )
    )

    with pytest.raises(ValueError):
        service.login(
            LoginRequest(
                email="mohamed@test.com",
                password="WrongPassword",
            )
        )


def test_login_unknown_email(db):
    service = AuthService(db)

    with pytest.raises(ValueError):
        service.login(
            LoginRequest(
                email="unknown@test.com",
                password="Password123",
            )
        )