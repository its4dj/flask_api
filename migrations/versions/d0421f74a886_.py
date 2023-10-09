"""empty message

Revision ID: d0421f74a886
Revises: 52bb6a8a6979
Create Date: 2023-10-07 11:12:42.829749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0421f74a886'
down_revision = '52bb6a8a6979'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mobile', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_model', schema=None) as batch_op:
        batch_op.drop_column('mobile')

    # ### end Alembic commands ###
