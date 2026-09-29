from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated, TypeAlias
import models
from database import SessionLocal
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from .auth import get_current_user




router = APIRouter(
    prefix="/users",
    tags=["users"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency: TypeAlias = Annotated[Session, Depends(get_db)]
user_dependency: TypeAlias = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency,
                    db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return db.query(models.Users).filter(models.Users.id == user.get("user_id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                          db: db_dependency,
                          user_password: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get("user_id")).first()
    if not bcrypt_context.verify(user_password.old_password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect")
    user_model.hashed_password = bcrypt_context.hash(user_password.new_password)
    db.add(user_model)
    db.commit()