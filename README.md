# Personal Expense Tracker – Backend

## 1. Project Overview

This repository contains the backend of the Personal Expense Tracker Web Application.

The backend is developed using Python and FastAPI. It provides REST APIs for user authentication and expense management and connects to a PostgreSQL database.

## 2. Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT Authentication
- Uvicorn

## 3. Main Features

- User registration API.
- User login API.
- JWT-based authentication.
- Create expense API.
- Retrieve expense records.
- Retrieve individual expense details.
- Update expense API.
- Delete expense API.
- PostgreSQL database integration.
- Database migrations using Alembic.

## 4. Database Structure

### Users Table

- id
- name
- email
- hashed_password

### Expenses Table

- id
- user_id
- amount
- category
- date
- description

## 5. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /register | Register a new user |
| POST | /login | Authenticate a user |
| GET | / | Check backend status |
| GET | /expenses | Retrieve expenses |
| POST | /expenses | Create an expense |
| GET | /expenses/{expense_id} | Retrieve an expense |
| PUT | /expenses/{expense_id} | Update an expense |
| DELETE | /expenses/{expense_id} | Delete an expense |

## 6. Project Structure

```text
backend/
├── app/
│   ├── routers/
│   ├── models.py
│   ├── main.py
│   ├── database.py
│   └── config.py
├── alembic/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── Procfile
├── alembic.ini
└── requirements.txt
```

## 7. Installation and Setup

### Clone the repository

```bash
git clone https://github.com/ShraddhaThitte28/Personal_Expense_Tracker_Backend.git
```

### Navigate to the project

```bash
cd Personal_Expense_Tracker_Backend
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Configure your PostgreSQL connection and JWT secret. Never upload actual credentials to GitHub.

### Run database migrations

```bash
alembic upgrade head
```

### Start the backend server

```bash
uvicorn app.main:app --reload
```

## 8. API Documentation

Swagger UI:

http://127.0.0.1:8000/docs

## 9. Live Backend

https://personal-expense-tracker-backend-jdox.onrender.com/

## 10. Frontend Repository

https://github.com/ShraddhaThitte28/Personal_Expense_Tracker_Frontend

## 11. Conclusion

This backend provides the APIs and database operations required by the Personal Expense Tracker application. Developing this project provided practical experience in FastAPI, REST APIs, SQLAlchemy, PostgreSQL, JWT authentication and database migrations.