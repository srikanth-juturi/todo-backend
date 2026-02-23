"""add category length check constraint

Revision ID: 20260223_03
Revises: 20260223_02
Create Date: 2026-02-23 01:15:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260223_03"
down_revision: str | None = "20260223_02"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_todos_category_len",
        "todos",
        "LEN(category) <= 50",
    )


def downgrade() -> None:
    op.drop_constraint("ck_todos_category_len", "todos", type_="check")
