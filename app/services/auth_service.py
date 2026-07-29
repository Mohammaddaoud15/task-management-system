from sqlalchemy.orm import Session

from app.core.logging import logger
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, request: RegisterRequest) -> User:
        existing_user = self.user_repository.get_by_email(request.email)

        if existing_user:
            logger.warning(
                "Registration failed. Email already exists: %s",
                request.email,
            )
            raise ValueError("Email already registered.")

        user = User(
            full_name=request.full_name,
            email=request.email,
            hashed_password=hash_password(request.password),
        )

        user = self.user_repository.create(user)

        logger.info(
            "New user registered successfully: %s",
            user.email,
        )

        return user

    def login(self, request: LoginRequest) -> str:
        user = self.user_repository.get_by_email(request.email)

        if not user:
            logger.warning(
                "Login failed. User not found: %s",
                request.email,
            )
            raise ValueError("There is no user with this email.")

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            logger.warning(
                "Login failed. Invalid password for: %s",
                request.email,
            )
            raise ValueError("Invalid password.")

        logger.info(
            "User logged in successfully: %s",
            user.email,
        )

        return create_access_token(str(user.id))