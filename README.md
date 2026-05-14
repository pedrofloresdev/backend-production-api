# Backend Production API

A production-ready REST API built with FastAPI, PostgreSQL, and SQLAlchemy 2. Demonstrates authentication, CRUD design, schema migrations, structured logging, containerization, and a full pytest suite -- all patterns used in real backend engineering roles.

---

## What This Project Demonstrates

| Concern | Implementation |
| --- | --- |
| Auth | JWT Bearer tokens via `python-jose`, bcrypt password hashing |
| Config | `pydantic-settings` -- typed, validated, env-file aware |
| ORM | SQLAlchemy 2 declarative models with timezone-aware timestamps |
| Migrations | Alembic with auto-generated and hand-tuned revisions |
| API design | Correct HTTP semantics: 201 on create, 204 on delete, 401/403/404/409 |
| Pagination | `skip` / `limit` on every collection endpoint, capped at 100 |
| Logging | `logging.getLogger(__name__)` throughout -- no bare `print()` |
| Tests | pytest + SQLite in-memory, 25 tests, 94% coverage, under 10 s |
| Docker | Image with db healthcheck, migrations-before-start |

---

## Architecture

```text
app/
├── api/v1/endpoints/   # Route handlers (auth, users, posts)
├── core/               # Config (pydantic-settings) and JWT/bcrypt security
├── db/
│   ├── base.py         # Declarative Base
│   ├── session.py      # Engine + get_db dependency
│   └── models/         # SQLAlchemy ORM models
├── schemas/            # Pydantic v2 request / response models
└── main.py             # FastAPI app, lifespan, router registration
alembic/                # Database migration scripts
tests/                  # pytest suite (SQLite in-memory)
```

---

## API Reference

### Auth

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `/api/v1/login` | -- | Exchange credentials for JWT |

### Users

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `/api/v1/users` | -- | Register -- 201 Created, 409 on duplicate email |
| GET | `/api/v1/users` | Bearer | List users (paginated) |
| GET | `/api/v1/users/me` | Bearer | Current user profile |

### Posts

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `/api/v1/posts` | Bearer | Create post -- 201 Created |
| GET | `/api/v1/posts` | -- | List posts (paginated, public) |
| GET | `/api/v1/posts/{id}` | -- | Get post -- 404 if missing |
| PUT | `/api/v1/posts/{id}` | Bearer | Full replace -- 403 if not owner |
| PATCH | `/api/v1/posts/{id}` | Bearer | Partial update -- only supplied fields change |
| DELETE | `/api/v1/posts/{id}` | Bearer | Delete -- 204 No Content, 403 if not owner |

All collection endpoints accept `?skip=0&limit=20` (max 100).

---

## Data Model

### users

| Column | Type | Notes |
| --- | --- | --- |
| id | Integer PK | |
| email | String | unique, indexed, NOT NULL |
| hashed_password | String | bcrypt, NOT NULL |
| created_at | TIMESTAMPTZ | server default now() |
| updated_at | TIMESTAMPTZ | server default now(), auto-updated |

### posts

| Column | Type | Notes |
| --- | --- | --- |
| id | Integer PK | |
| title | String | NOT NULL, indexed |
| content | String | NOT NULL |
| owner_id | Integer FK | references users.id, NOT NULL, ON DELETE CASCADE, indexed |
| created_at | TIMESTAMPTZ | server default now() |
| updated_at | TIMESTAMPTZ | server default now(), auto-updated |

---

## Running Locally

### With Docker (recommended)

```bash
cp .env.example .env          # fill in SECRET_KEY at minimum
docker-compose up --build
```

The compose file waits for the Postgres healthcheck before starting the API. Alembic then runs `upgrade head` before uvicorn starts.

### Manual

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Configuration

All settings are loaded from the environment (or `.env` file) via `pydantic-settings`. Unknown keys are silently ignored (`extra="ignore"`), so legacy `.env` files won't break startup.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `DATABASE_URL` | Yes | -- | SQLAlchemy connection string |
| `SECRET_KEY` | Yes | -- | HMAC key for JWT signing |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | Token lifetime in minutes |

---

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term-missing
```

Tests use an in-memory SQLite database -- no external services needed. Coverage sits at **94%** across 25 tests and completes in under 10 seconds.

---

## Tech Stack

- **FastAPI** 0.134 -- async web framework
- **SQLAlchemy** 2.0 -- ORM with typed column declarations
- **Alembic** -- schema migrations
- **pydantic-settings** -- typed environment configuration
- **python-jose** -- JWT encoding / decoding
- **passlib[bcrypt]** -- password hashing
- **PostgreSQL** -- production database
- **Docker / Render** -- containerization and cloud deployment

---

## Author

Pedro Flores -- Backend Developer (Python | FastAPI | PostgreSQL)
[github.com/pedrofloresdev](https://github.com/pedrofloresdev)
