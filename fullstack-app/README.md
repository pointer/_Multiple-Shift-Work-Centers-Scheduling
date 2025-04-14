# Multiple Shift Scheduling System

A fullstack application for optimizing workforce scheduling across multiple work centers with different skill level requirements.

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