# Copilot Instructions (Backend)

## Scope
Applies to backend Python services for the Todo platform.

## Architecture Rules
- Maintain layered backend flow:
  - `app/api` for request/response transport only.
  - `app/services` for use-case orchestration.
  - `app/models` for persistence/domain entities.
  - `app/schemas` for I/O and validation schemas.
  - `app/core` for config, security, and shared infrastructure concerns.
- API layer must not directly access database internals; go through service layer.
- Services must not depend on HTTP framework objects (`Request`, `Response`) except at transport boundary.

## Python Conventions
- Use type hints on all public functions and service methods.
- Keep functions small and single-purpose; extract helpers when branching grows.
- Prefer explicit imports and explicit return values.
- Use datetimes in UTC consistently.

## Naming and File Organization
- Files/modules: `snake_case`.
- Classes/schemas: `PascalCase`.
- Functions/variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Endpoint names should be resource-oriented (`/todos`, `/todos/{todo_id}`).

## Validation and Error Contracts
- Validate request payloads with schemas before entering service logic.
- Return structured errors with stable contract:
  - `code` (machine-readable)
  - `message` (safe human-readable)
  - optional `details` (field-level info)
- Map domain/service exceptions to HTTP status in API boundary only.
- Do not leak internal exception text to clients.

## Persistence and Migration Discipline
- Any schema/model persistence change requires migration scripts and downgrade path.
- Do not edit old migrations after merge; create a new forward migration.
- Keep migrations idempotent where practical and safe for CI.
- Document data backfill steps when introducing non-nullable fields.

## Testing Rules
- Add unit tests for service rules and edge cases.
- Add API integration tests for endpoint contracts and status codes.
- Prefer fixtures/factories over duplicated setup.
- Mock only external systems (network, clock, third-party APIs), not core business logic.

## Security Standards
- Treat all incoming data as untrusted.
- Enforce authN/authZ in boundary and service guards as designed.
- Use parameterized queries/ORM-safe patterns; no string-built SQL.
- Never log secrets, tokens, or password-like values.

## Forbidden Shortcuts
- No business logic inside route handlers.
- No global mutable state for request-specific data.
- No broad `except Exception` that returns `200`/`500` without mapping.
- No skipping migrations by manual table edits in runtime code.
- No test-only conditionals in production code paths.

## Minimal Example Pattern
```python
# api layer
@router.post("/todos", response_model=TodoResponse)
def create_todo(payload: CreateTodoRequest, service: TodoService = Depends(get_todo_service)):
    try:
        todo = service.create_todo(payload)
        return TodoResponse.model_validate(todo)
    except TodoValidationError as exc:
        raise to_http_error(exc)
```
