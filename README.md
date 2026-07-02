<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:2e5dac&height=180&section=header&text=Job%20Search%20Management%20Dashboard&fontSize=32&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=FastAPI%20%7C%20PostgreSQL%20%7C%20JWT%20%7C%20Docker&descAlignY=58&descSize=16" width="100%"/>

</div>

A production-grade backend system for managing the full job application lifecycle. Built with a focus on clean architecture, security, and scalability — not just a CRUD app, but a structured platform that tracks companies, applications, and statuses with strict per-user data isolation.

---

## Features

- JWT-based authentication with register, login, and protected routes
- Full CRUD for companies and job applications
- Application status tracking (applied, interview, offer, rejected, etc.)
- Per-user data isolation enforced at the query level
- Database schema versioning via Alembic migrations
- Repository Pattern separating data access from business logic
- Input validation and data contracts enforced through Pydantic

---

## Architecture

```
client request
      |
      v
FastAPI router
      |
      v
Service layer (business logic)
      |
      v
Repository layer (data access)
      |
      v
SQLAlchemy ORM + PostgreSQL
```

The Repository Pattern keeps the data layer decoupled from business logic. Each resource (users, companies, applications) has its own repository, making the codebase easy to extend and test independently.

---

## API Overview

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |

### Companies
| Method | Endpoint | Description |
|---|---|---|
| GET | `/companies` | List all companies for current user |
| POST | `/companies` | Add a new company |
| PUT | `/companies/{id}` | Update company details |
| DELETE | `/companies/{id}` | Delete a company |

### Applications
| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications` | List all applications for current user |
| POST | `/applications` | Create a new application |
| PATCH | `/applications/{id}/status` | Update application status |
| DELETE | `/applications/{id}` | Delete an application |

---

## Data Model

```
users
  └── companies (one user → many companies)
        └── applications (one company → many applications)
```

Each user sees only their own data. Foreign key relationships are enforced at the database level, and SQLAlchemy ORM handles all queries through the repository layer.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic |
| Auth | JWT (python-jose) |
| Containerization | Docker (in progress) |
| Frontend | React Dashboard (planned) |

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/NickH12/JobTracker
cd JobTracker

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

The API docs are available at `http://localhost:8000/docs` via FastAPI's auto-generated Swagger UI.

---

## Roadmap

- Docker Compose setup for full local environment
- React dashboard for visual job tracking
- Email notifications on status changes
- Analytics view (applications per company, conversion rates)

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2e5dac,100:1a1a2e&height=120&section=footer" width="100%"/>
</div>
