"""upgrade

Revision ID: 59a830daf7bb
Revises: 68722f7a20e5
Create Date: 2025-07-10 12:50:28.661173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59a830daf7bb'
down_revision: Union[str, Sequence[str], None] = '68722f7a20e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('task_model_user_id_fkey'), 'task_model', type_='foreignkey')
    op.drop_column('task_model', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_model', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key(op.f('task_model_user_id_fkey'), 'task_model', 'user_table', ['user_id'], ['id'])
    # ### end Alembic commands ###
