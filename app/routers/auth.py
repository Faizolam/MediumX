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



# +---------+       +---------------------------+      +-----------------------------------------------------+
# | /login  | ----> |OAuth2PasswordRequestForm  | ---> |user_credentials.username, user_credentials.password |
# +---------+       +---------------------------+      +-----------------------------------------------------+
#                                                                             |
#                                                                             |
#                                                                             v
#                                                           +------------------------------+        +-----------------------------------------------------------------+
#                                                           |if verify password in utils.py| --->  | oauth2.create_access_token(data=user.id) and return access_token |
#                                                           +------------------------------+        +-----------------------------------------------------------------+
#                                                                                                                    |
#                                                                                                    now whenerver you access api where get_current_user is used,
#                                                                                                  it will verify the access token and return the user data of that token
#                                                                                                                    v
#                                                                                                  +--------------------------------------------------+
#                                                                                                  |get_current_user get the token from oauth2_schema |
#                                                                                                  |OAuth2PasswordBearer(tokenUrl = 'login')          |
#                                                                                                  |  and pass it to verify_access_token fun          |
#                                                                                                  +--------------------------------------------------+
#                                                                                                                    |
#                                                                                                                    v
#                                                                                                  +--------------------------------------------------------+
#                                                                                                  |verify_access_token decode the token and return user id |
#                                                                                                  +--------------------------------------------------------+
#                                                                                                                    |
#                                                                                                                    v
#                                                                                                  +----------------------------------------------------------------+
#                                                                                                  |get user data from db using the user id and return it to the api|
#                                                                                                  +----------------------------------------------------------------+
# So the login fun is responsible for authenticating the user and generating an access token, while the get_current_user fun is responsible for verifying the access token and retrieving the current user's data based on that token.
# When a user logs in, they receive an access token. Whenever they make a request to an endpoint that requires authentication, the get_current_user function will be called to verify the token and retrieve the user's information.
# For example, if you have an endpoint that requires the current user's information, you would use get_current_user as a dependency in that endpoint. This way, the endpoint will only be accessible to authenticated users, and you can easily access the current user's data within that endpoint.

# over all, the login fun is responsible for authenticating the user and generating an access token, while the get_current_user fun is responsible for verifying the access token and retrieving the current user's data based on that token. This separation of concerns allows for a clean and modular authentication system in your FastAPI application.
# benifit of this approach is that it allows you to easily manage authentication and authorization in your application. By using JWT tokens, you can securely transmit user information between the client and server without having to store session data on the server. This makes your application more scalable and easier to maintain. Additionally, by separating the concerns of authentication and user retrieval, you can keep your code organized and easier to understand.
