from datetime import datetime, timedelta, timezone
import os
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import models
from sqlalchemy.orm import Session
from typing import Annotated, TypeAlias
from database import SessionLocal, engine
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt




router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

models.Base.metadata.create_all(bind=engine)


SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set"
    )
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency: TypeAlias = Annotated[Session, Depends(get_db)]





def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

class CreateUserRequest(BaseModel):
    
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=50)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=3, max_length=50)
    role: str = Field(min_length=3, max_length=50, default="user")
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    

async def get_current_user(token: Annotated[str, Depends(oauth_bearer)],
                           ):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        user_id : int = payload.get("user_id")
        role : str = payload.get("role")
        
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {"username": username, "user_id": user_id, "role": role}
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    

    
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: CreateUserRequest, 
                        db: db_dependency):
    existing_user = db.query(models.Users).filter((models.Users.username == user.username) | (models.Users.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    
    new_user = models.Users(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        role=user.role,
        isactive=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: db_dependency):
    
    user = db.query(models.Users).filter(models.Users.username == form_data.username).first()
    
    if not user or not bcrypt_context.verify(form_data.password, user.hashed_password):
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    encode = {"sub": user.username, "user_id": user.id, "role": user.role}
    expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    encode.update({"exp": expire})
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return Token(access_token=token, token_type="bearer")



