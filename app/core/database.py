from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# SQLALCHENY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
# Dependency to get the database session for each request and ensure it is closed after the request is finished.
def get_db():
    db = SessionLocal() 
    try:
        yield db #This is the most important part. Unlike return, which ends a function immediately, yield says:
# "Here is the database connection. Use it for as long as you need!"
    finally:
        db.close()
# Once your route function is completely finished (or even if it crashes with an error), the code "wakes up" and moves to the finally block.
# db.close() sends the connection back to the pool.
# This prevents "leaking connections," which is a common bug that can crash your database if too many idle connections stay open.