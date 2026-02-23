# Branch Strategy

## Goals

- Keep delivery predictable for a small team.
- Keep history understandable for production support.
- Keep process light enough for a single-user app.

## Branches

- `main`: always releasable.
- `develop`: integration branch for ongoing work.
- `feature/<short-name>`: feature work (example: `feature/todo-v1`).
- `hotfix/<short-name>`: urgent production fixes.

## Rules

1. Branch from `develop` for features.
2. Use short-lived branches (prefer < 3 days open).
3. Open PR to `develop` with:
   - passing CI quality gate
   - at least one reviewer
   - no unresolved comments
4. Merge `develop` to `main` for release with a release PR.
5. Tag releases as `vMAJOR.MINOR.PATCH`.

## Commit Convention

Use conventional commit style:

- `feat: add todo create endpoint`
- `fix: handle empty todo title`
- `chore: update lint config`
