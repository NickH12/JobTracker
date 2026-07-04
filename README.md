<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:2e5dac&height=180&section=header&text=Job%20Search%20Management%20Dashboard&fontSize=32&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=FastAPI%20%7C%20PostgreSQL%20%7C%20JWT%20%7C%20Docker&descAlignY=58&descSize=16" width="100%"/>

![CI](https://github.com/NickH12/JobTracker/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

</div>

A production-grade backend system for managing the full job application lifecycle. Built with a focus on clean architecture, security, and scalability — not just a CRUD app, but a structured platform that tracks companies, applications, and statuses with strict per-user data isolation.

**Live demo:** [jobtracker-7riq.onrender.com/docs](https://jobtracker-7riq.onrender.com/docs)
> Hosted on Render's free tier — if it's been idle, the first request can take 30-50 seconds to wake up.

---

## Features

- JWT-based authentication with register, login, and protected routes
- Full CRUD for companies and job applications
- Application status tracking (applied, interview, offer, rejected, etc.)
- Notes attached to individual applications
- Basic analytics endpoint over a user's applications
- Per-user data isolation enforced at the query level
- Database schema versioning via Alembic migrations
- Repository Pattern separating data access from business logic
- Input validation and data contracts enforced through Pydantic
- Fully containerized with Docker Compose — API + PostgreSQL, one command
- Automated testing (unit + integration) and a CI/CD pipeline that only deploys green builds

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

Full interactive documentation is available at `/docs` (Swagger UI) and `/redoc`.

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive a JWT token |
| GET | `/auth/me` | Get the current authenticated user |

### Companies
| Method | Endpoint | Description |
|---|---|---|
| GET | `/companies` | List all companies for the current user |
| POST | `/companies` | Add a new company |
| GET | `/companies/{id}` | Get a single company |
| PUT | `/companies/{id}` | Update company details |
| DELETE | `/companies/{id}` | Delete a company |

### Applications
| Method | Endpoint | Description |
|---|---|---|
| GET | `/applications` | List all applications for the current user |
| POST | `/applications` | Create a new application |
| PATCH | `/applications/{id}/status` | Update application status |
| DELETE | `/applications/{id}` | Delete an application |

### Notes & Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET / POST | `/notes` | View and add notes on an application |
| GET | `/analytics` | Aggregate stats over the user's applications |

All endpoints except `/auth/register` and `/auth/login` require a Bearer token and
only ever return data belonging to the authenticated user.

---

## Data Model

```
users
  └── companies (one user → many companies)
        └── applications (one company → many applications)
              └── notes (one application → many notes)
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
| Auth | JWT (python-jose), bcrypt password hashing |
| Testing | pytest, httpx (FastAPI TestClient) |
| Lint | ruff |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions + Render (auto-deploy on green CI) |

---

## Getting Started (Docker — recommended)

```bash
git clone https://github.com/NickH12/JobTracker
cd JobTracker
docker-compose up --build
```

That's it — the API and PostgreSQL both start, migrations run automatically, and the
API is available at `http://localhost:8000/docs`.

### Running without Docker

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # fill in your own DB credentials
alembic upgrade head
uvicorn app.main:app --reload
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `DB_HOST` | Database host |
| `DB_PORT` | Database port (default `5432`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `JWT_SECRET_KEY` | Secret key used to sign JWT tokens |
| `JWT_ALGORITHM` | JWT signing algorithm (default `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes (default `30`) |

---

## Testing

```bash
pytest -v
```

Tests run against an isolated in-memory SQLite database and never touch the real
development database. The suite covers:

- Unit tests for the repository layer, using mocked DB sessions
- Integration tests for auth, companies, and applications
- A regression test verifying users can never see each other's data

---

## CI/CD Pipeline

On every push to `main`:

1. **GitHub Actions** installs dependencies, runs `ruff check .` for linting, then
   runs the full `pytest` suite.
2. If — and only if — those checks pass, **Render** automatically deploys the new
   version to production.

Broken code never reaches the live demo.

---

## Roadmap

- React dashboard for visual job tracking
- Email notifications on status changes
- Expanded analytics (conversion rates, time-to-response, charts)

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2e5dac,100:1a1a2e&height=120&section=footer" width="100%"/>
</div>
