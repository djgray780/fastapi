"""create post table

Revision ID: 34a6bce63cf8
Revises: 
Create Date: 2022-02-07 08:22:16.091088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "34a6bce63cf8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("posts")
    pass
0