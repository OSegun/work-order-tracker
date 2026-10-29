import pytest

import app.models as models
from app.routers.auth import bcrypt_context
from tests.utils import TestingSessionLocal, reset_tables


@pytest.fixture
def test_user():
    reset_tables()

    user = models.Users(
        username="testuser",
        email="test.user@test.example",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.close()
    yield user
    reset_tables()


@pytest.fixture
def test_todo(test_user):
    todo_data = models.Todos(
        title="Upwork",
        description="Apply to upwork jobs",
        priority=5,
        complete=False,
        owner_id=test_user.id,
    )

    db = TestingSessionLocal()
    db.add(todo_data)
    db.commit()
    db.close()
    yield todo_data
