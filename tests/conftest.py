import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


engine = create_engine(settings.DATABASE_URL + "_test")
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def overrides_get_db():
        db = session
        yield db
        
    
    app.dependency_overrides[get_db] = overrides_get_db
    with TestClient(app) as client:
        yield client
        
    app.dependency_overrides.clear()
    
    
@pytest.fixture
def test_user(client):
    
    user_data = {"email": "testuser@gmail.com", "password" : "password123"}
    res = client.post('/user', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"id" : test_user["id"]})
    
    
@pytest.fixture
def authorized_client(client, token):
    
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(test_user, session):
    
    posts =  [
        {
        "title": "First Post",
        "content": "This is the first post content.",
        "user_id": test_user["id"]
        },
        {
        "title": "Second Post",
        "content": "Another post body goes here.",
        "user_id": test_user["id"]
        },
        {
        "title": "Third Post",
        "content": "More content for testing.",
        "user_id": test_user["id"]
        }
    ]
    
    
    session.add_all([models.Post(**d) for d in posts])
    session.commit()
    
    yield session.query(models.Post).all()

    
    
    

    