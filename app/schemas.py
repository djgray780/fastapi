from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr


class PostBase(BaseModel):
    # The annotation-only declaration tells pydantic that this field is required.
    title: str
    content: str
    published: bool = True  # Defaults to True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
