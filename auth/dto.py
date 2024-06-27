from pydantic import BaseModel


class User4Auth(BaseModel):
    raw_init_data: str


class UserResponse(BaseModel):
    id: int
    username: str
    tg_id: int
    first_name: str
    last_name: str
    language_code: str
    tg_hash: str

