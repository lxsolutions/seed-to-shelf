

"""Initial traceability models

Revision ID: 20250825
Revises:
Create Date: 2025-08-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20250825'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create compliance_events table
    op.create_table(
        'compliance_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_ref', sa.String(length=50), nullable=False),
        sa.Column('cte_type', sa.String(length=20), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('ts', sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    # Create lot_lineage table
    op.create_table(
        'lot_lineage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lot_code', sa.String(length=50), unique=True, nullable=False),
        sa.Column('parent_lot_codes', sa.JSON(), server_default='[]'),
        sa.Column('child_lot_codes', sa.JSON(), server_default='[]'),
        sa.Column('order_ids', sa.JSON(), server_default='[]'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create traceability_config table
    op.create_table(
        'traceability_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=50), unique=True, nullable=False),
        sa.Column('value', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('traceability_config')
    op.drop_table('lot_lineage')
    op.drop_table('compliance_events')

