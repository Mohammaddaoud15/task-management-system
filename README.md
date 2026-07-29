# Task Management API

A production-style Task Management REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Docker Compose**, and **JWT Authentication**.

## Features

- User registration
- User login with JWT authentication
- Password hashing using bcrypt
- Create tasks
- View all your tasks
- View a task by ID
- Update tasks
- Delete tasks
- PostgreSQL database
- Dockerized application
- Automatic interactive API documentation

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Docker & Docker Compose
- JWT (python-jose)
- Passlib (bcrypt)
- Pydantic
- UV package manager

---

## Project Structure

```
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
├── .env.example
├── .gitignore
├── .python-version
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT |

### Tasks

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/tasks/` | Create task |
| GET | `/tasks/` | Get all tasks |
| GET | `/tasks/{task_id}` | Get task by ID |
| PATCH | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

All task endpoints require a valid Bearer Token.

---

## Running with Docker

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/task-management-system.git
cd task-management-system
```

### 2. Create a `.env` file

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/task_management_db
SECRET_KEY=your_secret_key_here
```

### 3. Build and start

```bash
docker compose up --build
```

The API will be available at

```
http://localhost:8000
```

---

## API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

## Authentication

1. Register a new account.
2. Login using `/auth/login`.
3. Copy the returned access token.
4. Open `/docs`.
5. Click **Authorize**.
6. Enter

```
Bearer <your_access_token>
```

or simply paste the token if using the built-in OAuth2 flow.

---

## Future Improvements

- Automated unit tests
- Database migrations with Alembic
- Pagination and filtering
- Search functionality
- Task categories
- Task reminders
- CI/CD pipeline

---

## License

This project was developed for educational purposes.