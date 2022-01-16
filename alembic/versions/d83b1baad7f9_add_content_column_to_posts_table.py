"""add content column to posts table

Revision ID: d83b1baad7f9
Revises: bf1fb1643a14
Create Date: 2022-01-16 11:29:59.568267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd83b1baad7f9'
down_revision = 'bf1fb1643a14'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
