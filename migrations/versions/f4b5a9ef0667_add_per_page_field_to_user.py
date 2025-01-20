"""add per_page field to user

Revision ID: f4b5a9ef0667
Revises: 4ec8f8709e4b
Create Date: 2025-01-20 10:39:34.744219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4b5a9ef0667'
down_revision = '4ec8f8709e4b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('per_page', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('per_page')

    # ### end Alembic commands ###