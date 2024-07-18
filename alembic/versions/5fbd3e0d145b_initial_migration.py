"""Initial migration

Revision ID: 5fbd3e0d145b
Revises: 
Create Date: 2024-07-16 11:28:50.686057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fbd3e0d145b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('water_quality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('ph_level', sa.Float(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('turbidity', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_water_quality_id'), 'water_quality', ['id'], unique=False)
    op.create_index(op.f('ix_water_quality_location'), 'water_quality', ['location'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_water_quality_location'), table_name='water_quality')
    op.drop_index(op.f('ix_water_quality_id'), table_name='water_quality')
    op.drop_table('water_quality')
    # ### end Alembic commands ###
