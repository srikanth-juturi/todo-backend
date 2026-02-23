"""add category to todo

Revision ID: 20260223_02
Revises: 20260223_01
Create Date: 2026-02-23 00:30:00.000000

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260223_02"
down_revision: str | None = "20260223_01"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "todos",
        sa.Column("category", sa.String(length=50), nullable=False, server_default=sa.text("'general'")),
    )


def downgrade() -> None:
    op.execute(
        """
        DECLARE @df_name NVARCHAR(128);
        SELECT @df_name = dc.name
        FROM sys.default_constraints dc
        JOIN sys.columns c
            ON c.default_object_id = dc.object_id
        JOIN sys.tables t
            ON t.object_id = c.object_id
        WHERE t.name = 'todos' AND c.name = 'category';

        IF @df_name IS NOT NULL
            EXEC('ALTER TABLE todos DROP CONSTRAINT [' + @df_name + ']');
        """
    )
    op.drop_column("todos", "category")
