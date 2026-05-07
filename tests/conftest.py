import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.db as db_module
import app.main as main_module
from app.db import Base, get_db
from app.auth import current_user
from app.models import User


@pytest.fixture()
def db_engine(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture()
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_engine, monkeypatch, db_session):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(db_module, "engine", db_engine, raising=False)
    monkeypatch.setattr(db_module, "SessionLocal", TestingSessionLocal, raising=False)
    monkeypatch.setattr(main_module, "engine", db_engine, raising=False)

    main_module.app.dependency_overrides[get_db] = override_get_db

    user = User(username="tester", email="tester@example.com", password="hashed")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    main_module.app.dependency_overrides[current_user] = lambda: user

    with TestClient(main_module.app) as c:
        yield c

    main_module.app.dependency_overrides.pop(get_db, None)
    main_module.app.dependency_overrides.pop(current_user, None)
