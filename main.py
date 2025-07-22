from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from schemas import TaskCreate, TaskOut, ProfileBase, ProfileOut, RecommendationRequest
import crud
from fastapi.middleware.cors import CORSMiddleware
from ml_model.knn_recommender import KNNRecommender
from datetime import date
from scheduler import start_scheduler

Base.metadata.create_all(bind=engine)
recommender = KNNRecommender()
# scheduler = BackgroundScheduler()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Startup: Train model + Start Scheduler
@app.on_event("startup")
def startup():
    db = SessionLocal()
    tasks = crud.get_tasks(db)
    start_scheduler()
    recommender.train([t.title for t in tasks])
    db.close()

@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()

# ✅ Your Routes (no change)
@app.post("/recommend")
def get_recommendations(request: RecommendationRequest, db: Session = Depends(get_db)):
    try:
        return {"recommendations": recommender.recommend(request.new_title)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks", response_model=list[TaskOut])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    created = crud.create_task(db, task)
    recommender.train([t.title for t in crud.get_tasks(db)])
    return created

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    return crud.update_task(db, task_id, task)

@app.get("/profile", response_model=ProfileOut)
def read_profile(db: Session = Depends(get_db)):
    return crud.get_profile(db)

@app.put("/profile", response_model=ProfileOut)
def update_profile(profile: ProfileBase, db: Session = Depends(get_db)):
    return crud.update_profile(db, profile)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return crud.delete_task(db, task_id)
