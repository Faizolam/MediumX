from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.commentModel import Comment as SQLAlchemyComment
from ..models.userModel import User as SQLAlchemyUser
from ..schemas.commentsSchemas import CommentCreate,CommentRead,UserOut


class CommentOperation:
    def __init__(self, db:Session) -> None:
        self.db = db

    def add_comment(self, post_id:int, comment:CommentCreate, user_id:int):
        comments = SQLAlchemyComment(user_id=user_id, post_id=post_id, **comment.model_dump())
        self.db.add(comments)
        self.db.commit()
        self.db.refresh(comments)
        return comments

   

    def get_comments(self, post_id: int):
        comments = (
            self.db.query(SQLAlchemyComment, SQLAlchemyUser)
            .join(SQLAlchemyUser, SQLAlchemyComment.user_id == SQLAlchemyUser.id, isouter=True)
            .filter(SQLAlchemyComment.post_id == post_id)
            .order_by(SQLAlchemyComment.comment_date.desc())
            .all()
        )

        # if comments:
        #     comment, user = comments

        #     result = CommentRead(comment=comment,
        #                          username=user.username
        #     )
        result = [
            CommentRead(
                comment=comment.comment,
                comment_date=comment.comment_date,
                user=UserOut(id=user.id, username=user.username)
            )
            for comment, user in comments
        ]

        return result

# if post_by_id:
#             post, likes_count, noComment_count = post_by_id
            
#             post_data = PostWithLikes(
#                 PostRead=PostRead.from_orm(post),
#                 likes=likes_count,
#                 noComment=noComment_count
#             )
#             return post_data