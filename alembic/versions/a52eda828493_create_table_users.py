"""create table users

Revision ID: a52eda828493
Revises:
Create Date: 2025-06-02 14:54:51.799981

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a52eda828493"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID, primary_key=True),
        sa.Column("email", sa.String, unique=True),
        sa.Column("name", sa.String),
        sa.Column("created_at", sa.DateTime),
    )


def downgrade():
    op.drop_table("users")
