"""init_table_links

Revision ID: 733f1077ed8f
Revises:
Create Date: 2025-01-31 13:11:06.912521

"""
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import MEDIUMINT
from alembic import op


# revision identifiers, used by Alembic.
revision = '733f1077ed8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bbb_links',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()),
        sa.Column('url', sa.String(255), unique=True, nullable=False),
        sa.Column('status', MEDIUMINT(unsigned=True), index=True, nullable=False, server_default=sa.text("0"))
    )


def downgrade():
    op.drop_table('bbb_links')
