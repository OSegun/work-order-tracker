from ast import mod
from urllib import response

import models
from main import app
from routers.auth import get_current_user
from routers.users import get_db
from fastapi import status
import pytest
from test.utils import (TestingSessionLocal, 
                        override_get_current_user, 
                        override_get_db, test_todo,
                        client, test_user)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"
    
    
    

def test_change_password_success(test_user):
    
    response = client.put("/users/password",
                          json={"old_password": "testpassword",
                                "new_password": "newpassword"})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    
def test_change_password_invalid(test_user):
    
    response = client.put("users/password",
                          json={"old_password": "tpassword",
                                "new_password": "newpassword"})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Password is incorrect"}
    
    
# def test_change_phone_number(test_user):
    
#     response = client.put()