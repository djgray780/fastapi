from pydantic import BaseModel
from datetime import datetime


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
