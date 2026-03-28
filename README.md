# ESE Todo Backend

A RESTful API built with Django REST Framework for a Todo application with JWT authentication, deployed on Render with PostgreSQL.

## Live Demo

- API Base: https://ese-todo-backend.onrender.com/api
- API Docs (Swagger): https://ese-todo-backend.onrender.com/api/docs/

> Note: Free tier on Render spins down after inactivity. First request may take ~50 seconds.

## Tech Stack

- Django 6.0 / Django REST Framework
- PostgreSQL (production) / SQLite (local development)
- Simple JWT for token-based authentication
- drf-spectacular for API documentation
- Gunicorn for production serving
- Deployed on Render

## Architecture

This is the middleware layer in a three-layer enterprise architecture:

    React Frontend → Django REST API (this repo) → PostgreSQL Database

The API handles authentication, authorisation, business logic, validation, and database communication.

## API Endpoints

### Authentication
| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| POST | /api/auth/register/ | No |
| POST | /api/auth/token/ | No |
| POST | /api/auth/token/refresh/ | No |
| GET | /api/auth/profile/ | Yes |
| PATCH | /api/auth/profile/ | Yes |

### Todos
| Method | Endpoint | Auth Required |
|--------|----------|---------------|
| GET | /api/todos/ | Yes |
| POST | /api/todos/ | Yes |
| GET | /api/todos/{id}/ | Yes |
| PUT | /api/todos/{id}/ | Yes |
| DELETE | /api/todos/{id}/ | Yes |

## Local Setup

1. Clone the repo and install dependencies
```bash
git clone https://github.com/Akram2005m/ese-todo-backend
pip install -r requirements.txt
```

2. Create a .env file
```
DEBUG=True
SECRET_KEY=your-secret-key-here
FRONTEND_URL=http://localhost:5173
```

3. Run migrations and start server
```bash
python manage.py migrate
python manage.py runserver
```

## Deployment (Render)

- Build Command: pip install -r requirements.txt && python manage.py migrate
- Start Command: gunicorn backend.wsgi:application
- Environment Variables: DATABASE_URL, SECRET_KEY, DEBUG, FRONTEND_URL

## Security

- Passwords hashed using Django PBKDF2
- JWT authentication on all protected endpoints
- Users can only access their own todos
- Secrets managed via environment variables

## AI Usage

Claude (Anthropic) was used to assist with debugging CORS, setting up PostgreSQL via dj-database-url, and troubleshooting deployment. All code was reviewed and integrated manually.
