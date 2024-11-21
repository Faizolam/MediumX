from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models import userModel
from ..schemas import userSchemas
from ..modelsOperaions.user import UserOpration
from ..core.database import get_db, engine
from .. import utils

userModel.Base.metadata.create_all(bind = engine)

router = APIRouter(
    prefix = "/users",
    tags= ["Users"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[userSchemas.UserRead])
def get_all_users(db: Session=Depends(get_db)):
    """Get all users only for admin"""
    userOpt = UserOpration(db)
    getUser = userOpt.get_users()
    return getUser

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=userSchemas.UserRead)
def get_user_id(id: int, db: Session=Depends(get_db)):
    """Get user by ID"""
    single_user = UserOpration(db).get_user(user_id=id)
    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    return single_user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=userSchemas.UserRead)
def create_user(user_data: userSchemas.UserCreate, db : Session=Depends(get_db)):
    """Create New user"""

    #Hash the password - user_data.password
    hashed_password = utils.hash(user_data.password)
    user_data.password = hashed_password
    
    userOpt = UserOpration(db)
    newUser = userOpt.get_create_user(user_data=user_data)
    return newUser