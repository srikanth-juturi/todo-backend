"""create todos table

Revision ID: 20260223_01
Revises: None
Create Date: 2026-02-23 00:00:00.000000

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260223_01"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("GETUTCDATE()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("GETUTCDATE()")),
    )
    op.create_index("ix_todos_created_at", "todos", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_todos_created_at", table_name="todos")
    op.drop_table("todos")
