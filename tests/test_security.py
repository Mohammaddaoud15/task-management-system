from jose import JWTError

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "MySecurePassword123"

    hashed = hash_password(password)

    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_password_success():
    password = "MySecurePassword123"

    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_failure():
    password = "MySecurePassword123"

    hashed = hash_password(password)

    assert verify_password("WrongPassword", hashed) is False


def test_create_access_token():
    token = create_access_token("1")

    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token():
    token = create_access_token("1")

    payload = decode_access_token(token)

    assert payload["sub"] == "1"


def test_decode_invalid_token():
    invalid_token = "this.is.not.a.valid.token"

    try:
        decode_access_token(invalid_token)
        assert False
    except JWTError:
        assert True