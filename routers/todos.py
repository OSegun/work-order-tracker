from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated, TypeAlias
import models
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user





router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

        
db_dependency: TypeAlias = Annotated[Session, Depends(get_db)]
user_dependency: TypeAlias = Annotated[dict, Depends(get_current_user)]




class TodoItem(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,
                   db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id')).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency,
                    db: db_dependency, 
                    todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    todo_item = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("user_id")).first()
    if todo_item is not None:
        return todo_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")


@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoItem, 
                      db: db_dependency,
                      user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    todo_item = models.Todos(**todo.model_dump(), owner_id=user.get('user_id'))
    
    db.add(todo_item)
    
    db.commit()
    #db.refresh(todo_item)
    return todo_item


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,
                      todo: TodoItem,
                      db: db_dependency, 
                      todo_id: int = Path(gt=0)
                      ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    
    todo_item = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("user_id")).first()
    if todo_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")

    todo_item.title = todo.title
    todo_item.description = todo.description
    todo_item.priority = todo.priority
    todo_item.complete = todo.complete
    
    db.add(todo_item)
    db.commit()
    
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db: db_dependency,
                      todo_id: int = Path(gt=0)
                      ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    todo_item = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("user_id")).first()
    if todo_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("user_id")).delete()
    db.commit()


