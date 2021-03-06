"""empty message

Revision ID: 761cd5011204
Revises: 
Create Date: 2020-09-22 14:05:56.871628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '761cd5011204'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('place',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_name', sa.String(length=100), nullable=True),
    sa.Column('place_address', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('operation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.Date(), nullable=True),
    sa.Column('end_time', sa.Date(), nullable=True),
    sa.Column('round_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('signals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('operation_id', sa.Integer(), nullable=True),
    sa.Column('bssid', sa.String(length=100), nullable=True),
    sa.Column('ssid', sa.String(length=100), nullable=True),
    sa.Column('frequency', sa.Integer(), nullable=True),
    sa.Column('signal_level', sa.Integer(), nullable=True),
    sa.Column('sample_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['operation_id'], ['operation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signals')
    op.drop_table('operation')
    op.drop_table('place')
    # ### end Alembic commands ###
