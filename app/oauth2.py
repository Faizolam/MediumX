from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .schemas import userSchemas
from .core.database import get_db
from .core.config import settings
from .models import userModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'login')


# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Create access token fun
def create_access_token(data:dict):
    to_encode = data.copy()

    # expire time
    expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    # create jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



# verify access token to give and take data
def verify_access_token(token:str, credentials_exception):
    try:
        # Decode jwt and extract the Id from payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # this id is coming from login fun access_token data
        id = payload.get("user_id")
        # id_str = str(id)
        # print(type(id_str))
        print(type(id))
        if id is None:
            raise credentials_exception
        
        token_data = userSchemas.TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    return token_data




def get_current_user(token:str = Depends(oauth2_schema), db: Session=Depends(get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)

    user = db.query(userModel.User).filter(userModel.User.id == token.id).first()

    return user

