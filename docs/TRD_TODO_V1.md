# TRD: Single-User Todo Application v1

## Architecture

### 1) System Context

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Database:** SQL Server Express (local/dev baseline)
- **Auth:** none (single-user local context)

### 2) Backend Module Boundaries (Route-Service-Repository)

#### Route Layer (`app/api/v1`)

- Responsibility: HTTP concerns only.
- Parses request payloads using Pydantic schemas.
- Calls service layer and maps domain errors to HTTP status codes.
- Must not contain SQLAlchemy queries.

#### Service Layer (`app/services`)

- Responsibility: business rules and orchestration.
- Enforces rules: title trim, non-empty, max length 200, update semantics.
- Owns transaction boundaries for create/update/delete use cases.
- Returns domain DTOs/entities and raises typed domain errors.

#### Repository Layer (`app/repositories` or `app/services` submodule in v1)

- Responsibility: data access and query composition.
- Encapsulates SQLAlchemy session operations.
- Provides stable methods used by services:
  - `create_todo(...)`
  - `list_todos(order="created_desc")`
  - `get_todo_by_id(id)`
  - `update_todo(id, patch)`
  - `delete_todo(id)`

### 3) Frontend Module Boundaries

- `src/features/todos`: view + feature state orchestration.
- `src/services`: API client adapter for backend contracts.
- `src/types`: shared API DTO typings (request/response).
- `src/components`: reusable UI components only (no backend coupling).

### 4) Cross-Layer Contracts

- API schema is the single source of truth between frontend and backend.
- Datetime fields serialized as ISO-8601 UTC strings.
- Error envelope shape is stable across all endpoints.

### 5) Error Handling

- Validation errors: `422` from request schema validation.
- Not found: `404` for missing todo id.
- Conflict/business rule violation (future use): `409`.
- Unhandled exception: `500` with generic safe message.

Standard error response:

```json
{
  "error": {
    "code": "TODO_NOT_FOUND",
    "message": "Todo not found",
    "details": null,
    "trace_id": "uuid"
  }
}
```

### 6) Logging and Observability

- Structured logs (JSON preferred) on backend with keys:
  - `timestamp`, `level`, `trace_id`, `route`, `method`, `status_code`, `latency_ms`.
- Log levels:
  - `INFO`: successful request summary.
  - `WARNING`: client errors (`4xx`) with validation context.
  - `ERROR`: server errors (`5xx`) with stack trace in dev only.
- Generate/pass a `trace_id` per request for correlation.

### 7) Performance Considerations

- Indexes:
  - PK index on `todos.id`.
  - Non-clustered index on `todos.created_at DESC` for list ordering.
- Query shape: list endpoint supports bounded pagination in implementation even if UI initially fetches all.
- Target budgets (local baseline):
  - CRUD single-item p95 <= 300 ms.
  - List up to 1,000 records p95 <= 500 ms.

## Data Model v1

### Table: `todos`

- `id` bigint identity primary key
- `title` nvarchar(200) not null
- `category` nvarchar(50) not null default `general`
- `is_completed` bit not null default 0
- `created_at` datetime2 not null default current UTC timestamp
- `updated_at` datetime2 not null default current UTC timestamp

### Constraints and Rules

- Title length <= 200 enforced at API validation and DB schema level.
- Title must be non-empty after trim (API/service validation).
- Category length <= 50 enforced at API validation and DB schema level.
- Category defaults to `general` for backward compatibility when omitted.
- `updated_at` updates on every mutable change.

## API Contracts v1

Base path: `/api/v1`

### POST `/todos`

Request:

```json
{
  "title": "Buy milk",
  "category": "home"
}
```

Response `201`:

```json
{
  "id": 1,
  "title": "Buy milk",
  "category": "home",
  "is_completed": false,
  "created_at": "2026-02-23T10:00:00Z",
  "updated_at": "2026-02-23T10:00:00Z"
}
```

### GET `/todos`

Response `200`:

```json
[
  {
    "id": 2,
    "title": "Write tests",
    "category": "general",
    "is_completed": true,
    "created_at": "2026-02-23T11:00:00Z",
    "updated_at": "2026-02-23T11:20:00Z"
  }
]
```

### PATCH `/todos/{id}`

Request (partial update):

```json
{
  "title": "Write more tests",
  "category": "work",
  "is_completed": false
}
```

Response `200`: todo object (same shape as create).

### DELETE `/todos/{id}`

- Response `204` (no body).

### Error Contract

- `422`: schema validation failures.
- `404`: unknown `id`.
- `500`: unexpected backend error.

## Test Strategy v1

### 1) Backend Tests (`pytest`, `httpx`, `pytest-asyncio`)

- **Unit Tests**
  - Service validation (trim, empty title rejection, max length).
  - Service update semantics (`updated_at` changes only on mutation).
  - Repository query ordering and not-found behavior.
- **API Integration Tests**
  - POST success and validation failure (`422`).
  - GET order: newest first.
  - PATCH partial updates and status toggling.
  - DELETE + post-delete not-found (`404`).
  - Error envelope shape consistency.
- **Migration Tests**
  - Alembic upgrade from base to head on clean DB.
  - Alembic downgrade rollback verification.

### 2) Frontend Tests (`Vitest`, `RTL`)

- Render todo list from mocked API payload.
- Add todo flow with valid input.
- Prevent submit on empty/whitespace title.
- Toggle complete/incomplete behavior.
- Edit and delete interactions.
- Error rendering for API `4xx/5xx` responses.

### 3) Contract and Regression Scope

- Shared TypeScript DTO tests to ensure payload compatibility.
- Snapshot or schema-based checks for API error and todo response shapes.
- Regression suite for all acceptance criteria before merge.

## Migration Plan for Category

### Goal

Add optional single category per todo without breaking v1 clients.

### Phase Plan

1. **Schema Introduction (Backward Compatible)**
   - Add `categories` table.
   - Add nullable `todos.category_id` FK.
   - Keep existing endpoints and fields unchanged.
2. **API Extension (Non-Breaking)**
   - Extend todo response with optional `category` object or `category_id`.
   - Accept optional `category_id` in create/update payloads.
3. **Frontend Incremental Adoption**
   - Feature flag category UI controls.
   - Preserve current flows when category is absent.
4. **Data Backfill and Validation**
   - No mandatory backfill needed due to nullable FK.
   - Add constraints once category behavior stabilizes.

### Compatibility Rules

- v1 clients must continue to function without sending category fields.
- New fields remain optional in responses during transition.
- Migration must be reversible via Alembic downgrade.

## CI/Quality Gates

### Backend Gates

- Formatting: `black --check .`
- Linting: `ruff check .`
- Typing: `mypy app`
- Tests: `pytest -q`

### Frontend Gates

- Linting/type check: `npm run lint` and `npm run typecheck`
- Unit/integration tests: `npm run test`
- Build validation: `npm run build`

### Pull Request Exit Criteria

- All CI checks pass.
- New/changed endpoints include tests.
- Migration script reviewed for upgrade/downgrade safety.
- API contract updates reflected in frontend service typings.

## Risks and Mitigations

1. **Risk:** SQL Server Express config drift across developers.
   - **Mitigation:** provide canonical local connection template and migration verification step in onboarding.
2. **Risk:** Contract drift between backend schemas and frontend types.
   - **Mitigation:** maintain shared DTO definitions/tests and enforce API contract checks in CI.
3. **Risk:** Over-scoping beyond MVP (auth, tags, due dates).
   - **Mitigation:** PR checklist enforces MVP-only scope and out-of-scope guardrails.
4. **Risk:** Performance degradation with growing todo volume.
   - **Mitigation:** index on `created_at`, bounded query patterns, and latency checks in QA.
5. **Risk:** Incomplete error handling causing inconsistent UX.
   - **Mitigation:** standardized error envelope + negative-path tests for all endpoints.