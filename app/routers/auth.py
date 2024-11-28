from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..core.database import get_db, engine
from ..schemas import userSchemas 
from ..models.userModel import User as SQLAlchemyUser
from ..import utils, oauth2


router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=userSchemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):

    user = db.query(SQLAlchemyUser).filter(SQLAlchemyUser.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token, "token_type":"Bearer"}