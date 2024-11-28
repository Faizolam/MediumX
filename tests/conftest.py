from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.core.config import settings
from app.core.database import get_db, Base
from app.models.postModel import Post
from app.models.userModel import User
from app.oauth2 import create_access_token

# Debugging output for connection string
# print(f"Connecting to database {settings.DATABASE_NAME_TEST} at {settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT} with user {settings.DATABASE_USERNAME}")

SQLALCHEMY_DATABASE_URL_TEST = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)   

@pytest.fixture
def test_user(client):
   user_data = {"username":"Faiz Alam","email": "faza@gmail.com", "password": "pass123"}
   res = client.post("/users/", json=user_data)
   
#    if res.status_code != 200:
#        print("Response JSON:", res.json())
   assert res.status_code == 201
#    print(res.json())
   new_user = res.json()
   new_user['password'] = user_data["password"]
   return new_user


@pytest.fixture
def test_user2(client):
   user_data = {"username":"Masnoon Kamina","email": "faiz@gmail.com", "password": "pass321"}
   res = client.post("/users/", json=user_data)
   
#    if res.status_code != 200:
#        print("Response JSON:", res.json())
   assert res.status_code == 201
#    print(res.json())
   new_user = res.json()
   new_user['password'] = user_data["password"]
   return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "First Title",
            "summary": "This is the summary for the first post.",
            "content": "This is the content of the first post. It contains detailed information.",
            "image_post": None,
            "published": True,
            "owner_id": test_user['id'], 
        },
        {
            "title": "Second Title",
            "summary": "Summary for the second post.",
            "content": "Content of the second post. It provides insights into various topics.",
            "image_post": "17319999541307.jpg", 
            "published": True,
            "owner_id": test_user['id'],
        },
        {
            "title": "Third Title",
            "summary": "Summary for the third post.",
            "content": "Content of the third post. This one discusses different aspects.",
            "image_post": None,
            "published": True, 
            "owner_id": test_user['id'],
        },
        {
            "title": "Fourth Title",
            "summary": "Summary for the fourth post.",
            "content": "Content of the fourth post. It covers additional details.",
            "image_post": "17319999541308.jpg",
            "published": True,
            "owner_id": test_user['id'],
        }
        # ,{
        #     "title": "Fifth Title",
        #     "summary": "Summary for the fifth post.",
        #     "content": "Content of the fifth post. It covers additional details.",
        #     "image_post": "17319999541309.jpg",
        #     "published": True,
        #     "owner_id": test_user2['id'],
        # }
    ]

    def create_post_model(post):
        return Post(**post)
    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)

    session.commit()
    posts = session.query(Post).all()
    return session.query(Post).order_by(Post.id.desc()).all()
    # return posts
