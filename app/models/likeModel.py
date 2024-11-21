from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..core.database import Base

class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

    like_user = relationship("User", back_populates="likes")
    
    like_post = relationship("Post", back_populates="likes")