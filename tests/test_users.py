import pytest
from jose import jwt
from app.schemas.userSchemas import UserRead, Token

from app.core.config import settings


@pytest.fixture
def test_user(client):
   user_data = {"username":"Faiz Alam","email": "faza@gmail.com", "password": "pass123"}
   res = client.post("/users/", json=user_data)
   
   assert res.status_code == 201
#    print(res.json())
   new_user = res.json()
   new_user['password'] = user_data["password"]
#    print(new_user)
   return new_user



def test_create_user(client):
   res=client.post("/users/", json={"username":"Faiz Alam","email": "faza@gmail.com", "password": "pass123"})
    # print(res.json())
   assert res.status_code == 201

   # Optionally check the response data
   new_user = UserRead(**res.json())
   assert new_user.username == "Faiz Alam"
   assert new_user.email == "faza@gmail.com"


def test_login_user(test_user, client):
   res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
   print(res.json())
   login_res = Token(**res.json())
   payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
   id = payload.get("user_id")
   assert id == test_user["id"]
   assert login_res.token_type == "Bearer"
   assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code",[
#     ('wrongemail@gmail.com', 'password123', 403),
#     ('sanjeev@gmail.com', 'wrongpassword', 403),
#     ('wrongemail@gmail.com', 'wrongpassword', 403),
#     (None, 'password123', 422),
#     ('sanjeev@gmail.com', None, 422)
# ])
# def test_incorrect_login(client, email, password, status_code):
#    res = client.post("/login", data={"username":email, "password":password})

#    assert res.status_code == status_code
#    assert res.json().get("detail") == "Invalid Credentials"


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    # Prepare the data dictionary
    data = {"username": email, "password": password}

    # Send POST request
    res = client.post("/login", data=data)

    # Check for status code
    assert res.status_code == status_code

    # Handle responses based on status code
    if status_code == 422:  # Unprocessable Entity
        assert "detail" in res.json()  # Ensure there's a detail key
        assert isinstance(res.json()["detail"], list)  # It should be a list of errors
    elif status_code == 403:  # Forbidden
        # print(res.json())
        assert res.json().get("detail") == "Invalid Credentials"