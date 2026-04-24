# Telesecreter

A telemedicine appointment management system with a FastAPI backend and React frontend. The system allows managing doctors, patients, and appointments through a clean dashboard interface.

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, SQLite, Alembic  
**Frontend:** React, Vite, React Router, TanStack Query, Axios

## Architecture

The backend follows Clean Architecture with CQRS:

```
Telesecreter_API/           — FastAPI routers, dependency injection
Telesecreter_Application/   — Queries, commands, DTOs
Telesecreter_Domain/        — Entities, interfaces, enums
Telesecreter_Infrastructure/ — SQLAlchemy models, repositories, migrations
```

## Getting Started

### Backend

**Requirements:** Python 3.11+

```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed sample data
python Telesecreter_Infrastructure/seeds/db_seeds.py

# Start the API server
uvicorn Telesecreter_API.main:app --reload
```

API runs at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Frontend

**Requirements:** Node.js 18+

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Set VITE_API_BASE_URL=http://localhost:8000

# Start the dev server
npm run dev
```

Frontend runs at `http://localhost:5173`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctors/` | List all doctors |
| GET | `/doctors/{id}` | Get doctor by ID |
| GET | `/doctors/search?name=` | Search doctors by name |
| GET | `/users/` | List all users |
| GET | `/users/{id}` | Get user by ID |
| GET | `/appointments/` | List all appointments |
| GET | `/departments/` | List all departments |
| GET | `/scheduales/` | List all schedules |

## Project Structure

```
TelesecreterV1/
├── Telesecreter_API/          — API layer
├── Telesecreter_Application/  — Application layer
├── Telesecreter_Domain/       — Domain layer
├── Telesecreter_Infrastructure/ — Infrastructure layer
├── frontend/                  — React application
├── data/                      — SQLite database (gitignored)
├── requirements.txt
└── alembic.ini
```
