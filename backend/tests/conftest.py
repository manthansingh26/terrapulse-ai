"""
Shared test fixtures for TerraPulse AI backend tests.

Uses an in-memory SQLite database so tests run without PostgreSQL.
"""

import os
import sys
from pathlib import Path

# Ensure backend root is on sys.path
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# Override environment BEFORE any app module is imported
os.environ["DATABASE_URL"] = "sqlite:///./test_terrapulse.db"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["DEBUG"] = "false"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db.database import Base, get_db
from app.main import app

TEST_DB_URL = "sqlite:///./test_terrapulse.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    # Clean up test db file
    db_file = Path("test_terrapulse.db")
    if db_file.exists():
        try:
            db_file.unlink()
        except PermissionError:
            pass


@pytest.fixture()
def db_session():
    """Provide a clean database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    """Provide a test client with the database dependency overridden."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
