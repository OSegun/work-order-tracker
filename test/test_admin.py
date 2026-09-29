from ast import mod

import models
from main import app
from routers.auth import get_current_user
from routers.admin import get_db
from fastapi import status
import pytest
from test.utils import (TestingSessionLocal, 
                        override_get_current_user, 
                        override_get_db, test_todo,
                        client)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all(test_todo):
    response = client.get("admin/todo")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1,
            "title": "Upwork",
            "description": "Apply to upwork jobs",
            "priority": 5,
            "complete": False,
            "owner_id": 1,}]
    
    
def test_admin_delete_todo(test_todo):
    response = client.delete("admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    model = db.query(models.Todos).filter(models.Todos == 1).first()
    assert model is None
    

def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    #assert response.json() == []