# PRD: Single-User Todo Application (MVP)

## Objectives

- Deliver a simple, reliable single-user Todo application for local use.
- Enable core todo lifecycle: create, view, update, complete/uncomplete, delete.
- Keep MVP scope minimal: no authentication, no category support in v1.
- Define a clean path for post-MVP category enhancement without rework.

## Personas

- **Primary User (Individual Planner):** tracks personal tasks, needs low-friction task management.
- **Developer:** implements frontend and backend consistently with measurable behavior.
- **QA/Reviewer:** validates functional and non-functional criteria with clear pass/fail checks.

## User Stories

1. As a user, I want to add a todo with a short title so I can capture tasks quickly.
2. As a user, I want to see all my todos in one list so I can review my workload.
3. As a user, I want to mark a todo complete/incomplete so I can track progress.
4. As a user, I want to edit a todo title so I can correct or refine tasks.
5. As a user, I want to delete a todo so I can remove irrelevant items.

## Functional Requirements

1. **Create Todo**
   - User can create a todo with required `title`.
   - Title validation: trimmed, non-empty, max length 200.
2. **List Todos**
   - System returns all todos for the single local user.
   - Default sort: newest first by `created_at`.
3. **Update Todo**
   - User can update `title` and/or `is_completed`.
   - Partial updates supported.
4. **Delete Todo**
   - User can delete a todo by id.
5. **State Model**
   - Todo fields: `id`, `title`, `is_completed`, `created_at`, `updated_at`.
6. **Category Handling**
   - MVP: categories are explicitly out of scope.
   - Enhancement-ready: API and schema design should allow adding category relation in a later version.

## Non-Functional Requirements

1. **Performance**
   - API p95 latency for single-item CRUD endpoints <= 300 ms on local SQL Server Express (development machine baseline).
   - Todo list response p95 <= 500 ms for up to 1,000 todos.
2. **Reliability**
   - CRUD endpoints return correct HTTP status codes and stable JSON schema.
   - No data loss on normal create/update/delete operations.
   - Database migrations are repeatable and reversible via Alembic.
3. **Maintainability**
   - Backend layering respected (`api` -> `services` -> `models`).
   - Type hints and schema validation are used for public API contracts.
   - Migration scripts and API contracts documented for reviewers.

## Data Needs

### MVP Entities

- **Todo**
  - `id`: integer/bigint primary key
  - `title`: nvarchar(200), required
  - `is_completed`: bit, default false
  - `created_at`: datetime2, required
  - `updated_at`: datetime2, required

### Future Enhancement (Post-MVP)

- **Category** (planned)
  - `id`, `name`, timestamps
- **Todo.category_id** nullable FK to `Category.id` (or junction table if multi-category is later required)

## API Summary

Base path: `/api/v1`

- `POST /todos` -> create todo
- `GET /todos` -> list todos
- `PATCH /todos/{id}` -> update title and/or completion
- `DELETE /todos/{id}` -> delete todo

Response format: JSON with deterministic fields matching schemas.

## Acceptance Criteria

1. Creating a todo with valid title returns `201` and persisted record.
2. Creating a todo with empty/whitespace title returns `422` validation error.
3. Listing todos returns `200` with newest-first ordering.
4. Updating `title` returns `200` and updates `updated_at`.
5. Updating `is_completed` toggles status correctly and returns `200`.
6. Deleting an existing todo returns `204`; subsequent fetch/update/delete for same id returns `404`.
7. API contracts are covered by automated tests (unit/integration) with >= 90% pass rate in CI (all planned tests pass).
8. Alembic migration creates todo table successfully on clean database.
9. MVP UI supports add/list/edit/toggle/delete flows without authentication.
10. No category field appears in MVP UI or API payload contracts.

## Risks

- SQL Server Express local setup differences may cause migration/connection issues.
- Over-scoping risk (adding categories or auth too early) can delay MVP.
- Inconsistent frontend/backend contract naming can create avoidable defects.
- Lack of seed/test data can reduce QA confidence in list/update edge cases.

## Milestones

1. **M1 - API Foundation**
   - FastAPI project wiring, SQLAlchemy models, Alembic initial migration.
2. **M2 - Todo CRUD Backend**
   - Implement and test `/todos` endpoints with validation and error handling.
3. **M3 - Frontend MVP Flows**
   - Implement React views for add/list/edit/toggle/delete and service integration.
4. **M4 - QA and PR Readiness**
   - Execute quality gates, verify acceptance criteria, finalize review notes.

## Out of Scope (MVP)

- Authentication/authorization
- Multi-user support
- Categories, tags, priorities, due dates, reminders
- File attachments
- Real-time sync, push notifications
- Cloud deployment and production SLO commitments