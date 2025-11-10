from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="manager")  # manager / worker

    properties = relationship("Property", back_populates="manager")


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    manager = relationship("User", back_populates="properties")
    tasks = relationship("Task", back_populates="property", cascade="all,delete")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="Pending")  # Pending / In Progress / Done
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    assigned_to = Column(String, nullable=True)  # worker email or name
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)

    property = relationship("Property", back_populates="tasks")
    photos = relationship("TaskPhoto", back_populates="task", cascade="all,delete")


class TaskPhoto(Base):
    __tablename__ = "task_photos"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    url = Column(String, nullable=False)
    photo_type = Column(String, default="before")  # before / after

    task = relationship("Task", back_populates="photos")
