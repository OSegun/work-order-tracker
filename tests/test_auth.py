from datetime import timedelta

import pytest
from fastapi import HTTPException, status
from jose import jwt

from app.main import app
from app.routers.auth import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_db,
)
from tests.utils import TestingSessionLocal, override_get_current_user, override_get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_authenticate_user(test_user):

    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "testpassword", db)

    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("WrongUserName", "testpassword", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False

    db.close()


def test_create_access_token():

    username = "testuser"
    user_id = 1
    role = "user"
    expire_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expire_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signture": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "user_id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "user_id": 1, "role": "admin"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():

    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate credentials"
