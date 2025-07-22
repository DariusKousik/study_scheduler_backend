from sqlalchemy.orm import Session
from models import Task, Profile
import schemas
from schemas import TaskCreate, ProfileBase
from fastapi import HTTPException
import models

def get_tasks(db: Session):
    return db.query(Task).all()

def create_task(db: Session, task: TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_profile(db: Session):
    return db.query(Profile).first()

def update_profile(db: Session, data: ProfileBase):
    profile = db.query(Profile).first()
    if profile:
        profile.name = data.name
        profile.email = data.email
        profile.study_hours = data.study_hours
    else:
        profile = Profile(**data.dict())
        db.add(profile)
    db.commit()
    return profile

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = task.title
    db_task.date = task.date
    db_task.completed = task.completed

    db.commit()
    db.refresh(db_task)
    return db_task
