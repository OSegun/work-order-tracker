from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from alembic import command
from app.main import app
from app.settings import settings

SQLALCHEMY_DATABASE_URL = settings.test_database_url

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not set")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)


def _migrate_test_database() -> None:
    """Build the test schema with Alembic, so every run exercises the migrations."""
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    command.upgrade(alembic_config, "head")


_migrate_test_database()


def override_get_current_user():
    return {"username": "testuser", "user_id": 1, "role": "admin"}


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def reset_tables() -> None:
    """
    Empty both tables and restart their identity counters at 1
    """
    with engine.begin() as conn:
        conn.execute(
            text("""TRUNCATE TABLE todos, users RESTART IDENTITY CASCADE;""")
        )


client = TestClient(app)
