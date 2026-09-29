from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base
import models, pytest
from fastapi.testclient import TestClient
from main import app
from routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_current_user():
    return {"username": "testuser", "user_id": 1, "role": "admin"}


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
        
client = TestClient(app)


@pytest.fixture
def test_todo():
    todo_data = models.Todos(
        title="Upwork",
        description="Apply to upwork jobs",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo_data)
    db.commit()
    yield todo_data
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()
        
        

@pytest.fixture
def test_user():
    
    user = models.Users(
        
        username = "testuser",
        email="test.user@test.example",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
    )
    
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()
        
