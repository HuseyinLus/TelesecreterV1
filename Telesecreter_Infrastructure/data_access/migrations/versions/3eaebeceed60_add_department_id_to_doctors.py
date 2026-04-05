"""add department_id to doctors

Revision ID: 3eaebeceed60
Revises: c2a7cdd538a3
Create Date: 2026-04-05 14:12:26.773799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eaebeceed60'
down_revision: Union[str, Sequence[str], None] = 'c2a7cdd538a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department_id', sa.String(), nullable=False))
        batch_op.create_foreign_key('fk_doctors_department_id', 'departments', ['department_id'], ['id'])

def downgrade() -> None:
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_constraint('fk_doctors_department_id', type_='foreignkey')
        batch_op.drop_column('department_id')
