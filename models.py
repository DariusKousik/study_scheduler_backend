from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    date = Column(String)
    completed = Column(Boolean, default=False) 

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    study_hours = Column(Integer)
