"""add last few columns to posts table

Revision ID: 25fbf7d8102b
Revises: 362569232811
Create Date: 2022-01-16 12:04:52.717285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25fbf7d8102b'
down_revision = '362569232811'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column(
        "published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column(
        "created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")))
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
