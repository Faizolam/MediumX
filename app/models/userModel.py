from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from ..core.database import Base

# class Author(Base):
#     __tablename__ = "authors"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(100), nullable=False)
#     email = Column(String(50), nullable=False, unique=True)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    # user_role = Column(String(50), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # author_id = Column(Integer, ForeignKey('authers.id'))

    # posts = relationship('Post',foreign_keys="[Post.user_id]", back_populates='user', lazy=Tr
    posts = relationship("Post", back_populates="user")
    
    comments = relationship('Comment', back_populates='comment_user')

    likes = relationship("Like", back_populates="like_user")




    
    # comments = relationship('Comment', back_populates='users', lazy=True)
    # likes = relationship('Like', back_populates='user', lazy=True)
    # shares = relationship('Share', back_populates='user', lazy=True)
# from .postModel import Post
# from .commentModel import Comment

# CREATE TABLE Authors (
#     AuthorID INT PRIMARY KEY,
#     Name VARCHAR(100),
#     Email VARCHAR(50) UNIQUE
# );

# CREATE TABLE Users (
#     UserID INT PRIMARY KEY,
#     UserName VARCHAR(100),
#     UserEmail VARCHAR(50) UNIQUE,
#     UserRole VARCHAR(50),
#     UserPassword VARCHAR(100)
# );