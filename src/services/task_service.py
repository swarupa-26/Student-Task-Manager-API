from sqlalchemy.orm import Session
from ..repositories import task_repo
from ..models.task import Task, StatusEnum
from ..schemas.task import TaskCreate, TaskUpdate
from uuid import uuid4


def create_task(db: Session, payload: TaskCreate) -> Task:
    task = Task(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description,
        status=payload.status.value if payload.status else StatusEnum.pending.value,
        due_date=payload.due_date,
    )
    return task_repo.add_task(db, task)


def list_tasks(db: Session):
    return task_repo.list_tasks(db)


def get_task(db: Session, task_id: str):
    return task_repo.get_task(db, task_id)


def update_task(db: Session, task_id: str, payload: TaskUpdate):
    task = task_repo.get_task(db, task_id)
    if not task:
        return None

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(task, key, value)

    return task_repo.update_task(db, task)


def delete_task(db: Session, task_id: str) -> bool:
    task = task_repo.get_task(db, task_id)
    if not task:
        return False
    task_repo.delete_task(db, task)
    return True


def complete_task(db: Session, task_id: str):
    task = task_repo.get_task(db, task_id)
    if not task:
        return None
    task.status = StatusEnum.completed.value
    return task_repo.update_task(db, task)
