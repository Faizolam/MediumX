from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.sql.functions import coalesce
from app.models.postModel import Post as SQLAlchemyPost
from ..models.likeModel import Like as SQLAlchemyLike
from ..models.commentModel import Comment as SQLAchemyComment
from app.schemas.postSchemas import PostCreate,PostUpdate,PostRead,PostWithLikes

class PostOpration:
    def __init__(self, db:Session) -> None:
        self.db = db

    # def get_post(self, search, limit, skip):
    def get_post(self,limit, skip, search):
        
        all_posts = (
            self.db.query(
                SQLAlchemyPost,
                coalesce(func.count(SQLAlchemyLike.post_id), 0).label("likes"),
                coalesce(func.count(SQLAchemyComment.post_id),0).label("noComment")
            )
            .join(SQLAlchemyLike, SQLAlchemyLike.post_id == SQLAlchemyPost.id,  isouter=True)
            .join(SQLAchemyComment, SQLAchemyComment.post_id == SQLAlchemyPost.id, isouter=True)
            .group_by(SQLAlchemyPost.id)
            .filter(or_(
                SQLAlchemyPost.title.contains(search), 
                SQLAlchemyPost.summary.contains(search)
            ))
            .order_by(SQLAlchemyPost.created_at.desc())
            .limit(limit=limit)
            .offset(skip)
            .all()
        )
        

        posts_with_likes = [PostWithLikes(PostRead=PostRead.from_orm(post), likes=likes_count, noComment=noComment_count) for post, likes_count, noComment_count in all_posts]

        return posts_with_likes


    
    def own_posts(self, owner_id):
        posts = self.db.query(SQLAlchemyPost).filter(SQLAlchemyPost.owner_id == owner_id).order_by(SQLAlchemyPost.created_at.desc()).all()
        return posts
    

    def get_post_by_id(self, post_id:int):
        post_by_id = self.db.query(
                SQLAlchemyPost,
                coalesce(func.count(SQLAlchemyLike.post_id), 0).label("likes"),
                coalesce(func.count(SQLAchemyComment.post_id),0).label("noComment")
            ).join(SQLAlchemyLike, SQLAlchemyLike.post_id == SQLAlchemyPost.id, isouter=True).join(SQLAchemyComment, SQLAchemyComment.post_id == SQLAlchemyPost.id, isouter=True).group_by(SQLAlchemyPost.id).filter(SQLAlchemyPost.id == post_id).first()
        
        if post_by_id:
            post, likes_count, noComment_count = post_by_id
            
            post_data = PostWithLikes(
                PostRead=PostRead.from_orm(post),
                likes=likes_count,
                noComment=noComment_count
            )
            return post_data


    def get_create_post(self, owner_id:int, post_data: PostCreate):
        newPost = SQLAlchemyPost(owner_id=owner_id, **post_data.model_dump())
        print(newPost)
        self.db.add(newPost)
        self.db.commit()
        self.db.refresh(newPost)
        return newPost
    
    def get_update_post(self, post_id:int, update_post: PostUpdate):
        post_query = self.db.query(SQLAlchemyPost).filter(SQLAlchemyPost.id == post_id)
        if not post_query.first():
            return None
        
        post_query.update(update_post.model_dump(), synchronize_session=False)
        self.db.commit()
        updated_post = post_query.first()
        return updated_post
    
    def get_delete_post(self, post_id: int):
        post_query = self.db.query(SQLAlchemyPost).filter(SQLAlchemyPost.id == post_id)
        del_post = post_query.first()
        
        if not del_post:
            return None
        
        return del_post
    
    def get_delete(self, post: SQLAlchemyPost):
        self.db.delete(post)
        self.db.commit()




    