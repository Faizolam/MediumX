from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, engine
from ..schemas import commentsSchemas
from ..models import commentModel
from typing import List
from ..modelsOperaions.comment import CommentOperation
from ..import oauth2

commentModel.Base.metadata.create_all(bind=engine)

router=APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

@router.post("/{post_id}", status_code=status.HTTP_201_CREATED, response_model=commentsSchemas.CommentCreate)
def comment(post_id:str, comment:commentsSchemas.CommentCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.id)
    commentOpt = CommentOperation(db)
    comments = commentOpt.add_comment(post_id=post_id, comment=comment, user_id=current_user.id)

    return comments

@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=List[commentsSchemas.CommentRead])
def get_comment(post_id:str, db: Session=Depends(get_db)):

    # print(current_user.id)
    commentOpt = CommentOperation(db)
    comments = commentOpt.get_comments(post_id=post_id)
    return comments