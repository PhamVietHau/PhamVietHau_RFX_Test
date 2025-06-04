"""create table message_recipients

Revision ID: 97529643ac5c
Revises: d03a2a3827dc
Create Date: 2025-06-02 15:03:02.462155

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "97529643ac5c"
down_revision: Union[str, None] = "d03a2a3827dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "message_recipients",
        sa.Column("id", postgresql.UUID, primary_key=True),
        sa.Column("message_id", postgresql.UUID, sa.ForeignKey("messages.id")),
        sa.Column("recipient_id", postgresql.UUID, sa.ForeignKey("users.id")),
        sa.Column("read", sa.Boolean),
        sa.Column("read_at", sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table("message_recipients")
