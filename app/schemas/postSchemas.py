from pydantic import BaseModel,ConfigDict
from datetime import datetime
from .userSchemas import UserRead,UserOut
from typing import Optional

class PostBase(BaseModel):
    title: str
    summary: str
    content: str
    image_post: Optional[str]=None
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostRead(PostBase):
   id: int
   created_at:datetime
   owner_id: int
   user: UserOut
   
   class Config:
        from_attributes = True


class PostWithLikes(BaseModel):
    PostRead: PostRead
    likes: int
    noComment: int

    class Config:
        from_attributes = True