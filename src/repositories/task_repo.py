from sqlalchemy.orm import Session
from ..models.task import Task


def add_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: str):
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session):
    return db.query(Task).order_by(Task.created_at).all()


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()


def update_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
