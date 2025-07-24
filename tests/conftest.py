import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from nikita.src.main import app
from nikita.src.database import Base

# SQLite database URL for testing
SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


# Fixture to generate a random user id
@pytest.fixture()
def recipes_id() -> uuid.UUID:
    """Generate a random user id."""
    return str(uuid.uuid4())


# Fixture to generate a user payload
@pytest.fixture()
def recipes_payload(recipes_id):

    return {
        "id": recipes_id,
        "name": "John",
        "time_to_cook": "time_to_cook",
        "description": "123 Farmville",
    }


@pytest.fixture()
def recipes_updated(recipes_id):
    """Generate an updated user payload."""
    return {
        "id": recipes_id,
        "name": "John",
        "time_to_cook": "time_to_cook",
        "description": "123 Farmville",
    }