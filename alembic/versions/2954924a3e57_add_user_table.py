"""add user table

Revision ID: 2954924a3e57
Revises: d7156e8a8fe2
Create Date: 2022-02-08 07:59:17.403764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2954924a3e57"
down_revision = "d7156e8a8fe2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
