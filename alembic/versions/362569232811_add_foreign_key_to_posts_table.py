"""add foreign-key to posts table

Revision ID: 362569232811
Revises: 3b00554381a2
Create Date: 2022-01-16 12:00:29.040240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '362569232811'
down_revision = '3b00554381a2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
     local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
