"""add foreign-key to posts table

Revision ID: 30cf919f5d29
Revises: 2954924a3e57
Create Date: 2022-02-08 08:11:02.411587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "30cf919f5d29"
down_revision = "2954924a3e57"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
