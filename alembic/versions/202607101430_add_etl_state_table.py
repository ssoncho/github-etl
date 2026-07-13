"""add etl_state table

Revision ID: e7a4b0c9d1f2
Revises: 269c9fd523dc
Create Date: 2026-07-09 16:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7a4b0c9d1f2"
down_revision: Union[str, Sequence[str], None] = "269c9fd523dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "etl_state",
        sa.Column("entity", sa.String(length=100), nullable=False),
        sa.Column("last_loaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("entity"),
    )


def downgrade() -> None:
    op.drop_table("etl_state")
