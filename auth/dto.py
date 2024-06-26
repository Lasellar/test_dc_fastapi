from pydantic import BaseModel


class User4Auth(BaseModel):
    username: str
    password: str | None = None
    hashed_password: str | None = None
    disabled: bool | None = False


class UserResponse(BaseModel):
    username: str
    hashed_password: str | None = None
    disabled: bool | None = False
