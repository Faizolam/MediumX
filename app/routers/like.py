from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..core.database import get_db, engine
from ..schemas import likeSchemas
from ..models import likeModel
from ..modelsOperaions.like import likeOperation
from ..import oauth2

likeModel.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)


@router.post("/", status_code = status.HTTP_201_CREATED)
def like(like: likeSchemas.Like, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    likeOpt = likeOperation(db)
    result=likeOpt.find_post(post_id=like.post_id, dir=like.dir, user_id=current_user.id)

    if (like.dir == 1):
        if result==True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already Liked on post {like.post_id}")
        return {"messsage": "successfully added like"}
    else:
        if result == False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")
        return{"message": "successfully deleted like"}


