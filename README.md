# Todo Backend

FastAPI backend for the single-user Todo v1 application.

## Tech Stack

- FastAPI
- SQLAlchemy ORM
- Alembic migrations
- SQL Server Express (primary local/dev database)

## Layered Architecture

- Route layer: `app/api/v1`
- Service layer: `app/services`
- Repository layer: `app/repositories`
- Domain model: `app/models`
- DTO/schema contracts: `app/schemas`
- Core concerns (config, DB, logging, errors): `app/core`

## Setup

1. Create and activate virtual environment.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -U pip
pip install -r requirements.txt
```

3. Configure environment.

```bash
copy .env.example .env
```

Update `DATABASE_URL` in `.env` for your SQL Server Express instance.

## Migrations

Apply initial schema migration:

```bash
alembic upgrade head
```

Rollback one revision:

```bash
alembic downgrade -1
```

## Run API

```bash
uvicorn app.main:app --reload
```

## Available Endpoints

- `GET /health`
- `POST /api/v1/todos`
- `GET /api/v1/todos`
- `PATCH /api/v1/todos/{todo_id}`
- `DELETE /api/v1/todos/{todo_id}`

## Test

```bash
pytest -q
```
