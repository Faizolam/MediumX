"""Adding image_post Column in posts table

Revision ID: 53c00c837b7d
Revises: edc24056085e
Create Date: 2024-11-20 19:04:20.220239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53c00c837b7d'
down_revision: Union[str, None] = 'edc24056085e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('image_post', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'image_post')
    pass
