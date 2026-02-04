from app import schemas
from app.config import settings
from jose import jwt
import pytest

def test_root(client):
    
    res = client.get('/')
    assert(res.json().get("message") == "hello worrrld")
    assert(res.status_code == 200)
    
    

def test_create_user(client):
    
    data = {"email": "user1@gmail.com", "password": "password123"}
    res = client.post('/user', json=data)
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    
    
def test_login(client, test_user):
    
    print(type(test_user))
    email = test_user["email"]
    password = test_user["password"]
    
    res = client.post('/login', data = {"username": email, "password": password})
    login_res = schemas.Token(**res.json())
    
    token = login_res.access_token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert(id == test_user["id"])
    assert res.status_code == 200
    
    

@pytest.mark.parametrize("test_email, test_password, status_code", [
    ("testuser@gmil.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "password123", 403),
    ("testuser@gmil.com", None, 422),
    (None, "password123", 422),
    (None, None, 422)
])
def test_incorrect_login(client, test_user, test_email, test_password, status_code):
    
    res = client.post('/login', data={"username": test_email,"password": test_password})
    
    assert res.status_code == status_code
    
    
    
    