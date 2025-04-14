# Multiple Shift Scheduling System

A fullstack application for optimizing workforce scheduling across multiple work centers with 
different skill level requirements.

This is concerned with an employee scheduling problem involving multiple shifts
and work centers, where employees belong to a hierarchy of categories having downward substitutability. 
An employee at a higher category may perform the duties of an employee at a lower category, but not vice versa. 
However, a higher category employee receives a higher compensation than a lower category employee. 
For a given work center, the demand for each category during a given shift is fixed for the weekdays, 
and may differ from that on weekends. 
Two objectives need to be achieved: 
   - The first is to find a minimum-cost workforce mix of categories of employees 
      that is needed to satisfy specified demand requirements, 
   - The second is to assign the selected employees to 
      shifts and work centers, taking into consideration their preferences for shifts, work centers, and off-days.
The problem is to determine a minimum-cost workforce mix of categories of employees that is needed to satisfy
specified demand requirements, and to assign the selected employees to shifts and work centers,
taking into consideration their preferences for shifts, work centers, and off-days.
A mixed-integer programming model is initially developed for the problem, based on
which a specialized scheduling heuristic is subsequently developed for the problem. 
Computational results reported reveal that the proposed heuristic determines solutions proven to lie 
within 92–99% of optimality for a number of realistic test problems.

Key words: employee scheduling, manpower scheduling, mixed-integer programming,
hierarchical workforce, scheduling algorithm.
## Features

- Employee management with skill categories and preferences
- Work center configuration with varying demand requirements
- Shift pattern definition and management
- Automated schedule optimization using mixed-integer programming
- Schedule visualization and cost analysis
- Support for different skill categories and downward substitution
- Preference-based scheduling (shift preferences, work center preferences, days off)

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy
- PuLP (optimization)
- SQLite database

### Frontend
- Vue.js 3
- Vuetify 3
- ECharts for visualization
- Vue Router
- Axios

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

1. Use the development startup script:
```bash
./dev-start.ps1
```

This will start both the backend and frontend development servers:
- Backend: http://localhost:8000
- Frontend: http://localhost:8080

2. Initialize the database with test data by making a POST request to:
```
http://localhost:8000/init-db
```

## Usage

1. Start by adding or modifying employees through the Employees page
2. Configure work centers and their demand requirements
3. Navigate to the Schedule page to:
   - Select a work center
   - Choose a date range
   - Generate and optimize schedules
   - View schedule statistics and visualizations

## API Documentation

The API documentation is available at:
```
http://localhost:8000/docs
```

## Schedule Optimization

The system uses the following constraints and preferences in optimization:

1. **Hard Constraints**
   - Meet minimum staffing requirements for each category
   - One shift per day per employee
   - Maximum 5 consecutive working days
   - Honor day-off preferences

2. **Soft Preferences (Cost Factors)**
   - Employee shift preferences
   - Work center preferences
   - Hourly rate optimization

3. **Category Rules**
   - Support for downward substitution (higher categories can fill lower category demands)
   - Proper distribution of skilled workers

## Development

### Backend Structure
- `src/app.py` - Main FastAPI application
- `src/models/` - Database models and schemas
- `src/services/` - Business logic and optimization
- `src/routes/` - API endpoints

### Frontend Structure
- `src/views/` - Main view components
- `src/components/` - Reusable UI components
- `src/services/` - API client and utilities
- `src/router/` - Route configuration