from fastapi import FastAPI

from app.routers import admin, auth, todos, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)
