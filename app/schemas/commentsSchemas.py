from pydantic import BaseModel
from .userSchemas import UserOut
from datetime import datetime

class CommentCreate(BaseModel):
    comment: str

    class Config:
        from_attributes = True

class CommentRead(BaseModel):
    comment: str
    comment_date:datetime
    user: UserOut

    class Config:
        from_attributes = True