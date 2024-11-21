from sqlalchemy.orm import Session
from app.models.userModel import User as SQLAlchemyUser
from app.schemas.userSchemas import UserCreate

class UserOpration:
    def __init__(self, db:Session) -> None:
        self.db = db

    def get_users(self):
        return self.db.query(SQLAlchemyUser).all()

    def get_user(self, user_id:int):
        user_by_id = self.db.query(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id).first()
        return user_by_id
    
    def get_create_user(self, user_data:UserCreate):
        newUser = SQLAlchemyUser(**user_data.model_dump())
        self.db.add(newUser)
        self.db.commit()
        self.db.refresh(newUser)
        return newUser