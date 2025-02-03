"""init_table_items

Revision ID: c8ef683768b4
Revises: 733f1077ed8f
Create Date: 2025-01-31 13:42:52.064838

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c8ef683768b4'
down_revision = '733f1077ed8f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bbb_items',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('url', sa.String(255), nullable=False),  # todo: add unique constraint(separate revision)
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('categories', sa.JSON),
        sa.Column('full_address', sa.String(255)),
        sa.Column('website', sa.String(255)),
        sa.Column('image_url', sa.String(255)),
        sa.Column('phone', sa.String(20)),
        sa.Column('fax', sa.String(20)),
        sa.Column('hours_of_operation', sa.JSON),
        sa.Column('bbb_rating', sa.String(2)),
        sa.Column('accredited_since', sa.Date),
        sa.Column('est_date', sa.Date),
        sa.Column('years_in_business', sa.Integer),
        sa.Column('social_media', sa.JSON),
        sa.Column('management', sa.JSON),
        sa.Column('contacts', sa.JSON),
        )


def downgrade():
    op.drop_table('bbb_items')
