"""empty message

Revision ID: 6560e2fd46d8
Revises: 87ee31881b8f
Create Date: 2023-10-14 11:15:46.574605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6560e2fd46d8'
down_revision = '87ee31881b8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dummy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_model')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_model',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('dob', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('mobile', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_model_pkey')
    )
    op.drop_table('dummy')
    # ### end Alembic commands ###
