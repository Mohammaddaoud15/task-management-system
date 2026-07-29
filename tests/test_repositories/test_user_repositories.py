from app.models.user import User
from app.repositories.user_repositories import UserRepository


def test_create_user(db):
    repository = UserRepository(db)

    user = User(
        full_name="Mohamed",
        email="mohamed@test.com",
        hashed_password="hashed_password",
    )

    created_user = repository.create(user)

    assert created_user.id is not None
    assert created_user.email == "mohamed@test.com"
    assert created_user.full_name == "Mohamed"


def test_get_user_by_email(db):
    repository = UserRepository(db)

    user = User(
        full_name="Mohamed",
        email="mohamed@test.com",
        hashed_password="hashed_password",
    )

    repository.create(user)

    found_user = repository.get_by_email("mohamed@test.com")

    assert found_user is not None
    assert found_user.email == "mohamed@test.com"


def test_get_missing_user_by_email(db):
    repository = UserRepository(db)

    user = repository.get_by_email("missing@test.com")

    assert user is None


def test_get_user_by_id(db):
    repository = UserRepository(db)

    user = User(
        full_name="Mohamed",
        email="mohamed@test.com",
        hashed_password="hashed_password",
    )

    created_user = repository.create(user)

    found_user = repository.get_by_id(created_user.id)

    assert found_user is not None
    assert found_user.id == created_user.id


def test_get_missing_user_by_id(db):
    repository = UserRepository(db)

    user = repository.get_by_id(9999)

    assert user is None
