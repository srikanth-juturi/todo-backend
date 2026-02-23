# Repository Standards

## Engineering Principles

- Prefer readability over cleverness.
- Keep modules focused and small.
- Add complexity only when needed by an active requirement.

## Backend Coding Standards

- Python version target: 3.11+.
- Type hints on public functions.
- Validation via Pydantic schemas.
- API routes in `app/api/v1`, business logic in `app/services`.

## Quality Gates (Target)

- Formatting: `black --check .`
- Linting: `ruff check .`
- Typing: `mypy app`
- Tests: `pytest -q`

## Pull Request Standards

- Small PRs with one concern.
- Include testing notes in PR description.
- Update docs when behavior changes.
