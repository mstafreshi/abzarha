"""user table add name and lang field

Revision ID: 5e3a3051aa0b
Revises: 4718a8f3998d
Create Date: 2025-01-17 11:52:03.040159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e3a3051aa0b'
down_revision = '4718a8f3998d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('lang', sa.String(length=2), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('lang')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
