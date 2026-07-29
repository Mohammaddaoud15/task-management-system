# Task Management API

A production-style Task Management REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Docker Compose**, and **JWT Authentication**.

---

## Features

- User registration
- User login with JWT authentication
- Password hashing using bcrypt
- Create tasks
- View all your tasks
- View a task by ID
- Update tasks
- Delete tasks
- PostgreSQL database with SQLAlchemy ORM
- Dockerized application using Docker Compose
- Environment-based configuration using Pydantic Settings
- Structured application logging
- Automatic interactive API documentation (Swagger & ReDoc)
- Comprehensive unit and integration test suite using Pytest

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Docker & Docker Compose
- JWT (python-jose)
- Passlib (bcrypt)
- Pydantic
- Pytest
- Uvicorn
- UV package manager

---

## Project Structure

```text
task-management-system/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── enums.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   ├── task_repositories.py
│   │   └── user_repositories.py
│   │
│   ├── routers/
│   │   ├── auth_router.py
│   │   └── task_router.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── base.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   │
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
│
├── tests/
│   ├── test_repositories/
│   │   ├── test_task_repositories.py
│   │   └── test_user_repositories.py
│   │
│   ├── test_routers/
│   │   ├── test_auth_router.py
│   │   └── test_task_router.py
│   │
│   ├── test_services/
│   │   ├── test_auth_service.py
│   │   └── test_task_service.py
│   │
│   ├── conftest.py
│   ├── test_security.py
│   └── test_dependencies.py
│
├── .env.example
├── .gitignore
├── .python-version
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive a JWT access token |

### Tasks

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PATCH | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

> **Note:** All task endpoints require a valid Bearer Token.

---

## Running with Docker

### 1. Clone the repository

```bash
git clone https://github.com/Mohammaddaoud15/task-management-system.git
cd task-management-system
```

### 2. Create a `.env` file

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/task_management_db
SECRET_KEY=your_secret_key_here
```

### 3. Build and start the application

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

---

## Running the Tests

### Run locally

```bash
uv run pytest
```

### Run inside Docker

```bash
docker compose exec backend uv run pytest
```

### Current Test Status

```
46 passed
```

The test suite covers:

- Security utilities
- Authentication dependency
- User repository
- Task repository
- Authentication service
- Task service
- Authentication router
- Task router

---

## API Documentation

Swagger UI:

```
http://localhost:8000/docs
```



---

## Authentication

1. Register a new account.
2. Login using `/auth/login`.
3. Copy the returned JWT access token.
4. Open `/docs`.
5. Click **Authorize**.
6. Enter:

```
Bearer <your_access_token>
```

or simply paste the token when using FastAPI's built-in OAuth2 authorization flow.

---

## Logging

The project uses Python's built-in `logging` module to record important application events, including:

- Successful user registration
- Successful and failed login attempts
- Task creation
- Task updates
- Task deletion
- Unauthorized or invalid task operations

---

## License

This project was developed for educational purposes.