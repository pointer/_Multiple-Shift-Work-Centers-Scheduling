from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_level = Column(Integer)
    hourly_rate = Column(Float)
    shift_preferences = Column(JSON)
    work_center_preferences = Column(JSON)
    day_off_preferences = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    schedules = relationship("Schedule", back_populates="employee")

class WorkCenter(Base):
    __tablename__ = "work_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weekday_demand = Column(JSON)  # Dictionary mapping category levels to required counts
    weekend_demand = Column(JSON)  # Dictionary mapping category levels to required counts
    available_shifts = Column(JSON)  # List of shift IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    schedules = relationship("Schedule", back_populates="work_center")

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_time = Column(String)  # Store as HH:MM format
    end_time = Column(String)    # Store as HH:MM format
    is_weekend = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    schedules = relationship("Schedule", back_populates="shift")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    work_center_id = Column(Integer, ForeignKey("work_centers.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="schedules")
    work_center = relationship("WorkCenter", back_populates="schedules")
    shift = relationship("Shift", back_populates="schedules")