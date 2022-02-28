"""add content column to post table

Revision ID: d7156e8a8fe2
Revises: 34a6bce63cf8
Create Date: 2022-02-08 06:25:49.254637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d7156e8a8fe2"
down_revision = "34a6bce63cf8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
