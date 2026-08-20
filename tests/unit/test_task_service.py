import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.services import task_service
from src.schemas.task import TaskCreate, TaskUpdate


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_task(db_session):
    payload = TaskCreate(title="Complete homework", description="Finish math")
    task = task_service.create_task(db_session, payload)

    assert task.id is not None
    assert task.title == "Complete homework"
    assert task.description == "Finish math"
    assert task.status == "pending"
    assert task_service.get_task(db_session, task.id) is not None


def test_list_tasks(db_session):
    payload1 = TaskCreate(title="Task one")
    payload2 = TaskCreate(title="Task two")
    task_service.create_task(db_session, payload1)
    task_service.create_task(db_session, payload2)

    tasks = task_service.list_tasks(db_session)
    assert len(tasks) == 2
    assert {task.title for task in tasks} == {"Task one", "Task two"}


def test_update_task(db_session):
    task = task_service.create_task(db_session, TaskCreate(title="Read book"))
    payload = TaskUpdate(status="completed")

    updated = task_service.update_task(db_session, task.id, payload)
    assert updated is not None
    assert updated.status == "completed"
    assert task_service.get_task(db_session, task.id).status == "completed"


def test_complete_task_idempotent(db_session):
    task = task_service.create_task(db_session, TaskCreate(title="Read book"))

    first = task_service.complete_task(db_session, task.id)
    second = task_service.complete_task(db_session, task.id)

    assert first.status == "completed"
    assert second.status == "completed"
    assert task_service.get_task(db_session, task.id).status == "completed"


def test_delete_task(db_session):
    task = task_service.create_task(db_session, TaskCreate(title="Review notes"))

    deleted = task_service.delete_task(db_session, task.id)
    assert deleted is True
    assert task_service.get_task(db_session, task.id) is None


def test_update_nonexistent_task_returns_none(db_session):
    payload = TaskUpdate(title="New title")
    result = task_service.update_task(db_session, "missing-id", payload)
    assert result is None


def test_complete_nonexistent_task_returns_none(db_session):
    result = task_service.complete_task(db_session, "missing-id")
    assert result is None
