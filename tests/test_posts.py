import pytest
from app.schemas.postSchemas import PostRead, PostWithLikes, PostCreate, PostUpdate

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return PostWithLikes(**post)
    posts_map = map(validate, res.json())
    # print(res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].PostRead.id == test_posts[0].id

def test_unauthorized_user_post_all_posts(client, test_posts):
    res = client.post("/posts/")
    # print(res)
    assert res.status_code == 401


def test_unauthorized_user_get_own_posts(client, test_posts):
    res = client.get("/posts/ofsingaluser")
    # print(res)
    assert res.status_code == 401

# get post unauthorized user can access too.
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    # print(res)
    assert res.status_code == 200

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{88888}")
    # print(res)
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = PostWithLikes(**res.json())
    # print(post)
    assert post.PostRead.id == test_posts[0].id
    assert post.PostRead.content == test_posts[0].content
    assert post.PostRead.title == test_posts[0].title


@pytest.mark.parametrize("title, summary, content, published", [
    ("awesome new title","awesome new summary", "awesome new content", True),
    ("favorite pizza", "pizza summary", "i love pepperoni", False),
    ("tallest skyscrapers", "skyscrapers summary", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, summary, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "summary":summary, "content": content, "published": published})
    
    create_post = PostCreate(**res.json())
    # print(create_post)
    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.summary == summary
    assert create_post.content == content
    assert create_post.published == published
    # assert create_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitary title", "summary": "This is a summary", "content": "Hi There"})
    
    create_post = PostCreate(**res.json())
    assert res.status_code == 201
    assert create_post.title == "arbitary title"
    assert create_post.summary == "This is a summary"
    assert create_post.content == "Hi There"
    assert create_post.published == True

def test_unauthorized_user_create_post_(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitary title", "summary": "This is a summary", "content": "Hi There"})
    print(res.status_code)
    assert res.status_code == 401

def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    print(res)
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{820011}")
    assert res.status_code == 404


def test_update_post(authorized_client, test_user, test_posts):
    data= {
        "title": "updated title",
        "summary": "This is a summary",
        "content": "Updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = PostUpdate(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_unauthorized_user_update_Post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}"
    )
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "summary": "This is a summary",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(
        f"/posts/{8001}", json=data
    )
    assert res.status_code == 404

# def test_delete_other_user_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f"/posts/{test_posts[3].id}")
#     assert res.status_code == 403

# @pytest.mark.parametrize("post_data", [
#     {"title": "awesome new title", "summary": "awesome new summary", "content": "awesome new content", "published": True},
#     {"title": "favorite pizza", "summary": "pizza summary", "content": "i love pepperoni", "published": False},
#     {"title": "tallest skyscrapers", "summary": "skyscrapers summary", "content": "wahoo", "published": True},
# ])
# def test_create_post(authorized_client, test_user, post_data):
#     # Validate input data using PostCreate
#     create_post = PostCreate(**post_data)  # This will raise a ValidationError if validation fails
    
#     # Send POST request to create a new post
#     res = authorized_client.post("/posts/", json=create_post.model_dump())
    
#     # Validate response using PostRead
#     created_post = PostRead(**res.json())
    
#     print(created_post)  # Debugging output to see what was created
    
#     # Check for successful creation
#     assert res.status_code == 201  
#     assert created_post.title == create_post.title
#     assert created_post.summary == create_post.summary
#     assert created_post.content == create_post.content
#     assert created_post.published == create_post.published
    
#     # Check owner_id from the created post instance
#     assert created_post.owner_id == test_user['id']  # Access owner_id correctly