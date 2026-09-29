

from fastapi import FastAPI, Depends, HTTPException, status, Path, Request
#from sqlalchemy.orm import Session
#from typing import Annotated
import models
from database import engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
#from pydantic import BaseModel, Field
from routers import auth, todos, admin, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND) 
#templates.TemplateResponse(request, "home.html")




