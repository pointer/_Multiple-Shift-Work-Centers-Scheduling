from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    name: str
    category_level: int
    hourly_rate: float
    shift_preferences: List[int] = []
    work_center_preferences: List[int] = []
    day_off_preferences: List[str] = []

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class WorkCenterBase(BaseModel):
    name: str
    weekday_demand: Dict[str, int]
    weekend_demand: Dict[str, int]
    available_shifts: List[int]

class WorkCenterCreate(WorkCenterBase):
    pass

class WorkCenter(WorkCenterBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ShiftBase(BaseModel):
    name: str
    start_time: str
    end_time: str
    is_weekend: bool = False

class ShiftCreate(ShiftBase):
    pass

class Shift(ShiftBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    employee_id: int
    work_center_id: int
    shift_id: int
    date: datetime

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class OptimizationRequest(BaseModel):
    work_center_id: int
    start_date: datetime
    end_date: datetime

class ScheduleResponse(BaseModel):
    date: str
    shifts: List[Dict[str, any]]
    employees: List[Dict[str, any]]