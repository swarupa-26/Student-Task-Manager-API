from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from ..schemas.task import TaskCreate, TaskResponse, TaskUpdate
from ..services import task_service
from ..db.config import get_db

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = task_service.create_task(db, payload)
    return task

@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def patch_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
    updated = task_service.update_task(db, task_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

@router.post("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: str, db: Session = Depends(get_db)):
    updated = task_service.complete_task(db, task_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated
