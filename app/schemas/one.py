#models/postModel.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from ..core.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    image_post= Column(String, nullable=True)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User", back_populates="posts")

    comments = relationship('Comment', back_populates='comment_post', cascade="all, delete")

    likes = relationship("Like", back_populates="like_post", cascade="all, delete")



#schemas/postSchema.py
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

#modelsOperation/post.py
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.sql.functions import coalesce
from app.models.postModel import Post as SQLAlchemyPost
from ..models.likeModel import Like as SQLAlchemyLike
from ..models.commentModel import Comment as SQLAchemyComment
from app.schemas.postSchemas import PostCreate,PostUpdate,PostRead,PostWithLikes

class PostOpration:
    def __init__(self, db:Session) -> None:
        self.db = db

    # def get_post(self, search, limit, skip):
    def get_post(self,limit, skip, search):
        
        all_posts = (
            self.db.query(
                SQLAlchemyPost,
                coalesce(func.count(SQLAlchemyLike.post_id), 0).label("likes"),
                coalesce(func.count(SQLAchemyComment.post_id),0).label("noComment")
            )
            .join(SQLAlchemyLike, SQLAlchemyLike.post_id == SQLAlchemyPost.id,  isouter=True)
            .join(SQLAchemyComment, SQLAchemyComment.post_id == SQLAlchemyPost.id, isouter=True)
            .group_by(SQLAlchemyPost.id)
            .filter(or_(
                SQLAlchemyPost.title.contains(search), 
                SQLAlchemyPost.summary.contains(search)
            ))
            .order_by(SQLAlchemyPost.created_at.desc())
            .limit(limit=limit)
            .offset(skip)
            .all()
        )
        

        posts_with_likes = [PostWithLikes(PostRead=PostRead.from_orm(post), likes=likes_count, noComment=noComment_count) for post, likes_count, noComment_count in all_posts]

        return posts_with_likes


    
    def own_posts(self, owner_id):
        posts = self.db.query(SQLAlchemyPost).filter(SQLAlchemyPost.owner_id == owner_id).order_by(SQLAlchemyPost.created_at.desc()).all()
        return posts
    

    def get_post_by_id(self, post_id:int):
        post_by_id = self.db.query(
                SQLAlchemyPost,
                coalesce(func.count(SQLAlchemyLike.post_id), 0).label("likes"),
                coalesce(func.count(SQLAchemyComment.post_id),0).label("noComment")
            ).join(SQLAlchemyLike, SQLAlchemyLike.post_id == SQLAlchemyPost.id, isouter=True).join(SQLAchemyComment, SQLAchemyComment.post_id == SQLAlchemyPost.id, isouter=True).group_by(SQLAlchemyPost.id).filter(SQLAlchemyPost.id == post_id).first()
        
        if post_by_id:
            post, likes_count, noComment_count = post_by_id
            
            post_data = PostWithLikes(
                PostRead=PostRead.from_orm(post),
                likes=likes_count,
                noComment=noComment_count
            )
            return post_data


    def get_create_post(self, owner_id:int, post_data: PostCreate):
        newPost = SQLAlchemyPost(owner_id=owner_id, **post_data.model_dump())
        print(newPost)
        self.db.add(newPost)
        self.db.commit()
        self.db.refresh(newPost)
        return newPost
    
    def get_update_post(self, post_id:int, update_post: PostUpdate):
        post_query = self.db.query(SQLAlchemyPost).filter(SQLAlchemyPost.id == post_id)
        if not post_query.first():
            return None
        
        post_query.update(update_post.model_dump(), synchronize_session=False)
        self.db.commit()
        updated_post = post_query.first()
        return updated_post
    
    def get_delete_post(self, post_id: int):
        post_query = self.db.query(SQLAlchemyPost).filter(SQLAlchemyPost.id == post_id)
        del_post = post_query.first()
        
        if not del_post:
            return None
        
        return del_post
    
    def get_delete(self, post: SQLAlchemyPost):
        self.db.delete(post)
        self.db.commit()


#routers/post.py
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import FileResponse
import shutil
import os
from datetime import datetime
from sqlalchemy import func
# from ..models.postModel import Post
from ..models import postModel, likeModel
from ..schemas import postSchemas
from ..modelsOperaions.post import PostOpration
from ..core.database import get_db, engine
from ..import oauth2

postModel.Base.metadata.create_all(bind=engine)


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", status_code=status.HTTP_200_OK, response_model= List[postSchemas.PostWithLikes])
# @router.get("/", status_code=status.HTTP_200_OK)
def get_posts(db : Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """Get all posts"""
    posts = PostOpration(db).get_post(limit=limit, skip=skip, search=search)
    return posts
    
@router.get("/display/{filename}",status_code=status.HTTP_200_OK)
async def download_file(filename: str):
    file_path = f"./Upload/images/{filename}"  # Replace with the actual directory
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg")
    return {"error": "File not found"}

@router.get("/ofsingaluser", status_code=status.HTTP_200_OK, response_model=List[postSchemas.PostRead])
def get_own_posts(db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    """Get you own posts"""

    posts = PostOpration(db).own_posts(owner_id=current_user.id)
    print(posts)
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=postSchemas.PostWithLikes)
def get_post_id(id: int, db : Session = Depends(get_db)):
    """Get Post by Id."""

    single_post =  PostOpration(db).get_post_by_id(post_id=id)
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return single_post
    
    

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=postSchemas.PostRead)
def create_posts(post_data: postSchemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """ This API use for create. """

    print(current_user.id)
    postOpt = PostOpration(db)
    newPost = postOpt.get_create_post(owner_id =current_user.id, post_data=post_data)
    # post_img = upload_image(UploadFile = File(...))
    return newPost

@router.post("/upload-image", status_code=status.HTTP_200_OK)
async def upload_image(file: UploadFile = File(...)):
    try:
        uniqueFileName=str(datetime.now().timestamp()).replace(".","")
        print(uniqueFileName)
        fileNamesplit=str(file.filename).split(".")
        print(fileNamesplit)

        ext = fileNamesplit[len(fileNamesplit)-1]
        finalFileName=f"{uniqueFileName}.{ext}"
        finalFilePath=f"Upload/images/{finalFileName}"
        #Make sure the image folder existes
        os.makedirs("Upload/images/",exist_ok=True)

        with open(finalFilePath, "wb")as buffer:
            content = await file.read()
            res=buffer.write(content)

    except Exception as e:
        return {"error": str(e)}
    
    return {"filename": finalFileName, "status":"Image uploaded Successfully","content":res}


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=postSchemas.PostRead)
def update_post(id:int, updated_data:postSchemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Use this to update your post"""

    print(current_user)
    postOpt= PostOpration(db)
    updated_post = postOpt.get_update_post(post_id=id, update_post=updated_data)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requsted action")
    return updated_post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """You can delete the post here."""

    print(current_user)
    postOpt = PostOpration(db)
    del_post = postOpt.get_delete_post(post_id=id)

    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requestd action")
    
    postOpt.get_delete(del_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 
