from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models import db_models, schemas
import pulp
from fastapi import HTTPException

class SchedulingValidationError(Exception):
    pass

class SchedulingService:
    def __init__(self, db: Session):
        self.db = db

    def validate_optimization_request(
        self,
        work_center_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> None:
        """Validate optimization request parameters"""
        # Check date range
        if start_date > end_date:
            raise SchedulingValidationError("Start date must be before end date")
        
        if (end_date - start_date).days > 31:
            raise SchedulingValidationError("Schedule period cannot exceed 31 days")
        
        # Validate work center exists and has proper configuration
        work_center = self.db.query(db_models.WorkCenter).filter(
            db_models.WorkCenter.id == work_center_id
        ).first()
        
        if not work_center:
            raise SchedulingValidationError("Work center not found")
        
        if not work_center.weekday_demand or not work_center.weekend_demand:
            raise SchedulingValidationError("Work center demand not properly configured")
        
        # Validate available employees
        employees = self.db.query(db_models.Employee).all()
        if not employees:
            raise SchedulingValidationError("No employees available for scheduling")
        
        return work_center, employees

    def optimize_workforce(
        self,
        work_center_id: int,
        start_date: datetime,
        end_date: datetime
    ):
        """
        Implements the mixed-integer programming model for workforce optimization
        with validation and error handling
        """
        try:
            # Validate request
            work_center, employees = self.validate_optimization_request(
                work_center_id, start_date, end_date
            )
            
            # Initialize optimization problem
            prob = pulp.LpProblem("WorkforceScheduling", pulp.LpMinimize)
            
            # Create date range
            dates = [(start_date + timedelta(days=x)) for x in range((end_date - start_date).days + 1)]
            
            # Decision variables
            assignments = pulp.LpVariable.dicts(
                "assign",
                ((e.id, d.strftime("%Y-%m-%d"), s) 
                 for e in employees 
                 for d in dates 
                 for s in work_center.available_shifts),
                cat='Binary'
            )
            
            # Objective function: Minimize total cost while considering preferences
            prob += pulp.lpSum(
                assignments[e.id, d.strftime("%Y-%m-%d"), s] * (
                    e.hourly_rate * 8 +  # Base cost
                    (0 if s in e.shift_preferences else 2) +  # Shift preference penalty
                    (0 if work_center_id in e.work_center_preferences else 2)  # Work center preference penalty
                )
                for e in employees 
                for d in dates 
                for s in work_center.available_shifts
            )
            
            # Constraints
            for date in dates:
                is_weekend = date.weekday() >= 5
                demand = work_center.weekend_demand if is_weekend else work_center.weekday_demand
                
                # Demand constraints for each category with downward substitution
                for category, needed in demand.items():
                    prob += pulp.lpSum(
                        assignments[e.id, date.strftime("%Y-%m-%d"), s]
                        for e in employees 
                        for s in work_center.available_shifts
                        if e.category_level >= int(category)  # Allow downward substitution
                    ) >= needed
                
                # One shift per day per employee constraint
                for e in employees:
                    prob += pulp.lpSum(
                        assignments[e.id, date.strftime("%Y-%m-%d"), s]
                        for s in work_center.available_shifts
                    ) <= 1
                    
                    # Day off preferences constraint
                    if date.strftime("%A") in e.day_off_preferences:
                        prob += pulp.lpSum(
                            assignments[e.id, date.strftime("%Y-%m-%d"), s]
                            for s in work_center.available_shifts
                        ) == 0
            
            # Maximum consecutive days constraint (5 days)
            for e in employees:
                for i in range(len(dates) - 5):
                    consecutive_days = dates[i:i+6]
                    prob += pulp.lpSum(
                        assignments[e.id, d.strftime("%Y-%m-%d"), s]
                        for d in consecutive_days
                        for s in work_center.available_shifts
                    ) <= 5
            
            # Solve the problem
            prob.solve()
            
            if pulp.LpStatus[prob.status] != 'Optimal':
                raise SchedulingValidationError(
                    "Could not find optimal solution. Please check demand requirements and available workforce."
                )
            
            # Convert solution to schedule
            schedule = []
            for date in dates:
                date_str = date.strftime("%Y-%m-%d")
                for e in employees:
                    for s in work_center.available_shifts:
                        if pulp.value(assignments[e.id, date_str, s]) == 1:
                            schedule.append(schemas.ScheduleCreate(
                                employee_id=e.id,
                                work_center_id=work_center_id,
                                shift_id=s,
                                date=date
                            ))
            
            # Save the schedule
            self._save_schedule(schedule)
            
            return schedule
            
        except SchedulingValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred during schedule optimization: {str(e)}"
            )

    def _save_schedule(self, schedule: List[schemas.ScheduleCreate]):
        """
        Save the optimized schedule to the database with error handling
        """
        try:
            # Clear existing schedule for the affected dates
            min_date = min(s.date for s in schedule)
            max_date = max(s.date for s in schedule)
            
            self.db.query(db_models.Schedule).filter(
                and_(
                    db_models.Schedule.date >= min_date,
                    db_models.Schedule.date <= max_date
                )
            ).delete(synchronize_session=False)
            
            # Insert new schedule
            for item in schedule:
                db_schedule = db_models.Schedule(
                    employee_id=item.employee_id,
                    work_center_id=item.work_center_id,
                    shift_id=item.shift_id,
                    date=item.date
                )
                self.db.add(db_schedule)
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save schedule: {str(e)}"
            )

    def get_schedule(
        self,
        work_center_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """
        Retrieve the schedule for a work center within a date range
        with additional statistics
        """
        try:
            schedules = self.db.query(db_models.Schedule).filter(
                and_(
                    db_models.Schedule.work_center_id == work_center_id,
                    db_models.Schedule.date >= start_date,
                    db_models.Schedule.date <= end_date
                )
            ).all()
            
            result = {}
            total_cost = 0
            
            for schedule in schedules:
                date_str = schedule.date.strftime("%Y-%m-%d")
                if date_str not in result:
                    result[date_str] = {
                        "date": date_str,
                        "shifts": [],
                        "employees": [],
                        "daily_cost": 0,
                        "categories": {}
                    }
                
                employee = self.db.query(db_models.Employee).get(schedule.employee_id)
                shift = self.db.query(db_models.Shift).get(schedule.shift_id)
                
                if shift.id not in [s["id"] for s in result[date_str]["shifts"]]:
                    result[date_str]["shifts"].append({
                        "id": shift.id,
                        "name": shift.name,
                        "start_time": shift.start_time,
                        "end_time": shift.end_time
                    })
                
                # Calculate daily cost
                daily_cost = employee.hourly_rate * 8  # Assuming 8-hour shifts
                result[date_str]["daily_cost"] += daily_cost
                total_cost += daily_cost
                
                # Track category counts
                category = str(employee.category_level)
                if category not in result[date_str]["categories"]:
                    result[date_str]["categories"][category] = 0
                result[date_str]["categories"][category] += 1
                
                result[date_str]["employees"].append({
                    "id": employee.id,
                    "name": employee.name,
                    "category_level": employee.category_level,
                    "shift_id": shift.id,
                    "hourly_rate": employee.hourly_rate
                })
            
            # Add summary statistics
            summary = {
                "total_cost": total_cost,
                "total_shifts": sum(len(day["employees"]) for day in result.values()),
                "average_daily_cost": total_cost / len(result) if result else 0,
                "category_utilization": self._calculate_category_utilization(result)
            }
            
            return {
                "schedule": result,
                "summary": summary
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve schedule: {str(e)}"
            )

    def _calculate_category_utilization(self, schedule: Dict) -> Dict[str, float]:
        """Calculate the utilization percentage for each category level"""
        total_shifts = sum(len(day["employees"]) for day in schedule.values())
        if not total_shifts:
            return {}
            
        category_counts = {}
        for day in schedule.values():
            for emp in day["employees"]:
                category = str(emp["category_level"])
                if category not in category_counts:
                    category_counts[category] = 0
                category_counts[category] += 1
        
        return {
            category: (count / total_shifts) * 100
            for category, count in category_counts.items()
        }