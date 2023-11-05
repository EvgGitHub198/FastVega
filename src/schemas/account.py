from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str


class User(BaseModel):
    email: str
    full_name: str

    class Config:
        from_attributes = True
