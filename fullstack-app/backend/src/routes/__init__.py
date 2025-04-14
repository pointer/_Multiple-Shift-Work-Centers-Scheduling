# backend/src/routes/__init__.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import schemas
from ..models import db_models
from ..services.scheduling import SchedulingService
from datetime import datetime

router = APIRouter()

# Employee routes
@router.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db_models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees/", response_model=List[schemas.Employee])
def get_employees(db: Session = Depends(get_db)):
    return db.query(db_models.Employee).all()

@router.get("/employees/{employee_id}", response_model=schemas.Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(db_models.Employee).filter(db_models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(db_models.Employee).filter(db_models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee.dict().items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(db_models.Employee).filter(db_models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"detail": "Employee deleted"}

# Work Center routes
@router.post("/work-centers/", response_model=schemas.WorkCenter)
def create_work_center(work_center: schemas.WorkCenterCreate, db: Session = Depends(get_db)):
    db_work_center = db_models.WorkCenter(**work_center.dict())
    db.add(db_work_center)
    db.commit()
    db.refresh(db_work_center)
    return db_work_center

@router.get("/work-centers/", response_model=List[schemas.WorkCenter])
def get_work_centers(db: Session = Depends(get_db)):
    return db.query(db_models.WorkCenter).all()

@router.get("/work-centers/{work_center_id}", response_model=schemas.WorkCenter)
def get_work_center(work_center_id: int, db: Session = Depends(get_db)):
    db_work_center = db.query(db_models.WorkCenter).filter(db_models.WorkCenter.id == work_center_id).first()
    if not db_work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    return db_work_center

@router.put("/work-centers/{work_center_id}", response_model=schemas.WorkCenter)
def update_work_center(work_center_id: int, work_center: schemas.WorkCenterCreate, db: Session = Depends(get_db)):
    db_work_center = db.query(db_models.WorkCenter).filter(db_models.WorkCenter.id == work_center_id).first()
    if not db_work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    for key, value in work_center.dict().items():
        setattr(db_work_center, key, value)
    
    db.commit()
    db.refresh(db_work_center)
    return db_work_center

@router.delete("/work-centers/{work_center_id}")
def delete_work_center(work_center_id: int, db: Session = Depends(get_db)):
    db_work_center = db.query(db_models.WorkCenter).filter(db_models.WorkCenter.id == work_center_id).first()
    if not db_work_center:
        raise HTTPException(status_code=404, detail="Work center not found")
    
    db.delete(db_work_center)
    db.commit()
    return {"detail": "Work center deleted"}

# Shift routes
@router.post("/shifts/", response_model=schemas.Shift)
def create_shift(shift: schemas.ShiftCreate, db: Session = Depends(get_db)):
    db_shift = db_models.Shift(**shift.dict())
    db.add(db_shift)
    db.commit()
    db.refresh(db_shift)
    return db_shift

@router.get("/shifts/", response_model=List[schemas.Shift])
def get_shifts(db: Session = Depends(get_db)):
    return db.query(db_models.Shift).all()

# Schedule routes
@router.get("/schedule/")
def get_schedule(
    work_center_id: int,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    scheduling_service = SchedulingService(db)
    return scheduling_service.get_schedule(
        work_center_id=work_center_id,
        start_date=datetime.strptime(start_date, "%Y-%m-%d"),
        end_date=datetime.strptime(end_date, "%Y-%m-%d")
    )

@router.post("/optimize/workforce")
def optimize_workforce(request: schemas.OptimizationRequest, db: Session = Depends(get_db)):
    scheduling_service = SchedulingService(db)
    try:
        schedule = scheduling_service.optimize_workforce(
            work_center_id=request.work_center_id,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return {"message": "Schedule optimized successfully", "schedule": schedule}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/init-db")
async def initialize_database(db: Session = Depends(get_db)):
    """Initialize database with test data"""
    try:
        # Create test shifts
        shifts = [
            db_models.Shift(
                name="Morning",
                start_time="06:00",
                end_time="14:00",
                is_weekend=False
            ),
            db_models.Shift(
                name="Afternoon",
                start_time="14:00",
                end_time="22:00",
                is_weekend=False
            ),
            db_models.Shift(
                name="Night",
                start_time="22:00",
                end_time="06:00",
                is_weekend=False
            ),
            db_models.Shift(
                name="Weekend Day",
                start_time="08:00",
                end_time="20:00",
                is_weekend=True
            )
        ]
        
        for shift in shifts:
            db.add(shift)
        db.commit()
        
        # Create test work centers
        work_centers = [
            db_models.WorkCenter(
                name="Assembly Line A",
                weekday_demand={
                    "1": 3,  # Category 1 workers needed
                    "2": 2,  # Category 2 workers needed
                    "3": 1   # Category 3 workers needed
                },
                weekend_demand={
                    "1": 2,
                    "2": 1,
                    "3": 1
                },
                available_shifts=[shift.id for shift in shifts]
            ),
            db_models.WorkCenter(
                name="Quality Control",
                weekday_demand={
                    "2": 2,
                    "3": 2
                },
                weekend_demand={
                    "2": 1,
                    "3": 1
                },
                available_shifts=[shift.id for shift in shifts]
            )
        ]
        
        for work_center in work_centers:
            db.add(work_center)
        db.commit()
        
        # Create test employees
        employees = [
            db_models.Employee(
                name="John Smith",
                category_level=3,
                hourly_rate=25.0,
                shift_preferences=[1, 2],  # Prefers morning and afternoon shifts
                work_center_preferences=[1],  # Prefers Assembly Line A
                day_off_preferences=["Saturday", "Sunday"]
            ),
            db_models.Employee(
                name="Jane Doe",
                category_level=2,
                hourly_rate=20.0,
                shift_preferences=[2, 3],  # Prefers afternoon and night shifts
                work_center_preferences=[1, 2],
                day_off_preferences=["Sunday", "Monday"]
            ),
            db_models.Employee(
                name="Bob Wilson",
                category_level=1,
                hourly_rate=18.0,
                shift_preferences=[1],  # Prefers morning shift
                work_center_preferences=[1],
                day_off_preferences=["Saturday"]
            ),
            # Add more test employees with different preferences and categories
            db_models.Employee(
                name="Alice Johnson",
                category_level=3,
                hourly_rate=25.0,
                shift_preferences=[1, 2],
                work_center_preferences=[2],
                day_off_preferences=["Sunday"]
            ),
            db_models.Employee(
                name="Charlie Brown",
                category_level=2,
                hourly_rate=20.0,
                shift_preferences=[3],
                work_center_preferences=[1, 2],
                day_off_preferences=["Saturday", "Sunday"]
            ),
            db_models.Employee(
                name="Diana Martinez",
                category_level=1,
                hourly_rate=18.0,
                shift_preferences=[1, 2],
                work_center_preferences=[1],
                day_off_preferences=["Monday"]
            )
        ]
        
        for employee in employees:
            db.add(employee)
        db.commit()
        
        return {"message": "Database initialized with test data"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize database: {str(e)}"
        )
