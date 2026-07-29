from datetime import datetime

from app.schemas.base import BaseSchema


class UserResponse(BaseSchema):
    id: int
    full_name: str
    email: str
    created_at: datetime
