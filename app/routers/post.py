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