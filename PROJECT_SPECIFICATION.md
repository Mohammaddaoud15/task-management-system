# Task Management System

## Project Goal

Develop a production-style backend Task Management System that demonstrates modern backend engineering practices using FastAPI.

The system should showcase:

- Clean Architecture
- RESTful API Design
- JWT Authentication
- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations
- Docker & Docker Compose
- Logging
- Unit Testing
- Configuration Management
- API Documentation

---

# Functional Requirements

## Authentication

Users can:

- Register
- Login
- Access protected endpoints using JWT

---

## Tasks

Authenticated users can:

- Create tasks
- View their tasks
- View a single task
- Update tasks
- Delete tasks

Each task contains:

- Title
- Description
- Status
- Priority
- Due Date
- Created At
- Updated At

---

## Authorization

- Every task belongs to exactly one user.
- Users cannot access tasks owned by another user.

---

## Validation

The API validates:

- Required fields
- Field lengths
- Email format
- Password constraints
- Invalid request bodies

---

## Error Handling

The API returns consistent error responses.

---

## Logging

The application logs:

- Startup
- Shutdown
- Authentication events
- Unexpected errors

---

## Testing

The project includes unit tests for:

- Authentication
- Business Logic
- API Endpoints

---

# Non-functional Requirements

The project should be:

- Maintainable
- Modular
- Well documented
- Containerized
- Easy to run
- Easy to test

---

# Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Docker Compose
- Pytest
- Pydantic