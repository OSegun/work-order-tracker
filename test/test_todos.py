import models
from main import app
from routers.auth import get_current_user
from routers.todos import get_db
from fastapi import status
import pytest
from test.utils import (TestingSessionLocal, 
                        override_get_current_user, 
                        override_get_db, test_todo,
                        client)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user





def test_read_all_authenticated_user(test_todo):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1,
            "title": "Upwork",
            "description": "Apply to upwork jobs",
            "priority": 5,
            "complete": False,
            "owner_id": 1,}]
    
    
def test_read_one_authenticated_user(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1,
            "title": "Upwork",
            "description": "Apply to upwork jobs",
            "priority": 5,
            "complete": False,
            "owner_id": 1,}
    
    
def test_read_one_authenticated_user_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo item not found"}
    
    
def test_create_todo(test_todo):
    new_todo = {
        "title": "New Todo",
        "description": "This is a new todo item",
        "priority": 3,
        "complete": False
    }
    response = client.post("/todos/todo/", json=new_todo)
    assert response.status_code == status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    created_todo = db.query(models.Todos).filter(models.Todos.id == 2).first()
    assert created_todo.title == new_todo["title"]
    assert created_todo.description == new_todo["description"]
    assert created_todo.priority == new_todo["priority"]
    assert created_todo.complete == new_todo["complete"]
    
    
def test_update_todo(test_todo):
    updated_todo = {
        "title": "Updated Todo",
        "description": "This is an updated todo item",
        "priority": 4,
        "complete": True
    }
    response = client.put("/todos/todo/1", json=updated_todo)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    updated_todo_item = db.query(models.Todos).filter(models.Todos.id == 1).first()
    assert updated_todo_item.title == updated_todo["title"]
    assert updated_todo_item.description == updated_todo["description"]
    assert updated_todo_item.priority == updated_todo["priority"]
    assert updated_todo_item.complete == updated_todo["complete"]


def test_todo_not_found():
    updated_todo = {
        "title": "Updated Todo",
        "description": "This is an updated todo item",
        "priority": 4,
        "complete": True
    }
    response = client.put("/todos/todo/999", json=updated_todo)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo item not found"}
    
    
def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSessionLocal()
    deleted_todo = db.query(models.Todos).filter(models.Todos.id == 1).first()
    assert deleted_todo is None
    
def test_delete_todo_not_found():
    response = client.delete("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo item not found"}