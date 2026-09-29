from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated, TypeAlias
import models
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user




router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency: TypeAlias = Annotated[Session, Depends(get_db)]
user_dependency: TypeAlias = Annotated[dict, Depends(get_current_user)]



@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency,
                         db: db_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return db.query(models.Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,
                      db: db_dependency,
                      todo_id: int = Path(gt=0)
                      ):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    todo_item = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found")
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()