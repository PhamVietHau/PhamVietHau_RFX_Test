"""create table message

Revision ID: d03a2a3827dc
Revises: a52eda828493
Create Date: 2025-06-02 14:59:29.716989

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d03a2a3827dc"
down_revision: Union[str, None] = "a52eda828493"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID, primary_key=True),
        sa.Column("sender_id", postgresql.UUID, sa.ForeignKey("users.id")),
        sa.Column("subject", sa.String, nullable=True),
        sa.Column("content", sa.Text),
        sa.Column("timestamp", sa.DateTime),
    )


def downgrade():
    op.drop_table("messages")
