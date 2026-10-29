from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String, unique=True)
    username: Mapped[str | None] = mapped_column(String, unique=True)
    hashed_password: Mapped[str | None] = mapped_column(String)
    isactive: Mapped[bool | None] = mapped_column(Boolean, default=True)
    role: Mapped[str | None] = mapped_column(String, default="user")


class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    priority: Mapped[int | None] = mapped_column(Integer)
    complete: Mapped[bool | None] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"))
