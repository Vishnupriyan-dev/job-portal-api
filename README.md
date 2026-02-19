# Job Portal API

Backend API system built using FastAPI and MySQL.

This project simulates a job portal platform supporting job seekers and recruiters. 
It follows a layered architecture separating controllers, services, and repository logic.

## Tech Stack

- Python
- FastAPI
- MySQL
- SQLAlchemy (Core with raw SQL queries)
- JWT Authentication
- Pydantic (Input Validation)

## Key Features

- User registration and login with JWT token generation
- Role-based access control for recruiter assignment
- Company and location management
- Skill management with experience range
- Dynamic job search with optional filters
- Application history and recent applications
- Soft delete strategy for user accounts
- Custom exception handling mapped to HTTP responses

## Architecture

Controller → Service → Repository → Database

- Controllers handle request/response.
- Services contain business logic.
- Repository layer executes parameterized SQL queries.
- Database connection handled via dependency injection.

## Running Locally

1. Set environment variables:

DB_USER  
DB_PASSWORD  
DB_HOST  
DB_NAME  

2. Install dependencies:

pip install -r requirements.txt

3. Run server:

uvicorn app.main:app --reload

Access Swagger UI at:

http://127.0.0.1:8000/docs

## Current Limitations

- Automated tests not implemented yet
- No pagination for job listings
- No deployment configuration included

