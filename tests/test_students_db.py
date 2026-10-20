from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base,get_db
from app.core.config import settings

from app.models.student import Student
from app.models.teacher import Teacher

import pytest

TEST_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database="student_teacher_test",
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db



Base.metadata.create_all(bind=test_engine)

client = TestClient(app)


@pytest.fixture
def student_payload():
    return {
        "name": "Arun",
        "age": 22,
        "email": "arun.test@example.com",
    }

