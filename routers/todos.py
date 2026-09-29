from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
from sqlalchemy.orm import Session
from typing import Annotated, TypeAlias
import models
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates




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
        
def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
        
db_dependency: TypeAlias = Annotated[Session, Depends(get_db)]
user_dependency: TypeAlias = Annotated[dict, Depends(get_current_user)]
templates = Jinja2Templates(directory="templates")


@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("user_id")).all()

        return templates.TemplateResponse(request, "todo.html", {"todos": todos, "user": user})

    except:
        return redirect_to_login()


@router.get('/add-todo-page')
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(request, "add-todo.html", {"user": user})

    except:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

        return templates.TemplateResponse(request, "edit-todo.html", {"todo": todo, "user": user})

    except:
        return redirect_to_login()


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
