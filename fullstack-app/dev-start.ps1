# Start backend server
Start-Process -NoNewWindow powershell -ArgumentList @(
    "cd ./backend;",
    "python -m uvicorn src.app:app --reload --port 8000"
)

# Start frontend development server
Start-Process -NoNewWindow powershell -ArgumentList @(
    "cd ./frontend;",
    "npm run serve"
)

Write-Host "Development servers started!"
Write-Host "Backend running at: http://localhost:8000"
Write-Host "Frontend running at: http://localhost:8080"
Write-Host ""
Write-Host "Initialize the database by making a POST request to: http://localhost:8000/init-db"