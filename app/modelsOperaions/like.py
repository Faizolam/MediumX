from sqlalchemy.orm import Session
from ..models.likeModel import Like as SQLAlchemyLike
from ..models.postModel import Post as SQLAlchemyPost
# from ..schemas.likeSchemas import Like


class likeOperation:
    def __init__(self, db:Session) -> None:
        self.db = db

    def find_post(self, post_id:int, dir:int, user_id:int):
        post = self.db.query(SQLAlchemyPost).filter(SQLAlchemyPost.id == post_id).first()
        if not post:
            return False
        vote_query = self.db.query(SQLAlchemyLike).filter(SQLAlchemyLike.post_id == post_id, SQLAlchemyLike.user_id == user_id) 
        found_like = vote_query.first()
        if dir == 1:
            if found_like:
                return True
            new_like = SQLAlchemyLike(post_id = post_id, user_id = user_id)
            self.db.add(new_like)
            self.db.commit()
            return {"messsage": "successfully added vote"}
        else:
            if not found_like:
                return False
            vote_query.delete(synchronize_session=False)
            self.db.commit()
            return{"message": "successfully deleted vote"}

    
