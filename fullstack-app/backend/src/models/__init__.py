from datetime import datetime, time
from typing import List, Optional
from pydantic import BaseModel

class ShiftPreference(BaseModel):
    shift_id: int
    preference_level: int  # 1-5, 5 being most preferred

class WorkCenterPreference(BaseModel):
    work_center_id: int
    preference_level: int

class DayOffPreference(BaseModel):
    day: str  # Monday, Tuesday, etc.
    preference_level: int

class Employee(BaseModel):
    id: Optional[int]
    name: str
    category_level: int
    hourly_rate: float
    shift_preferences: List[ShiftPreference]
    work_center_preferences: List[WorkCenterPreference]
    day_off_preferences: List[DayOffPreference]

class Shift(BaseModel):
    id: Optional[int]
    name: str
    start_time: time
    end_time: time
    is_weekend: bool

class WorkCenter(BaseModel):
    id: Optional[int]
    name: str
    weekday_demand: dict  # category_level: number_needed
    weekend_demand: dict
    available_shifts: List[int]  # shift_ids

class Schedule(BaseModel):
    id: Optional[int]
    employee_id: int
    work_center_id: int
    shift_id: int
    date: datetime
    created_at: datetime = datetime.now()