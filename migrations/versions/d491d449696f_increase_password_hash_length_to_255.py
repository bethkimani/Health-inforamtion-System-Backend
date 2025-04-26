"""Increase password_hash length to 255

Revision ID: d491d449696f
Revises: e8d3b18e360d
Create Date: 2025-04-26 21:25:15.413381
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd491d449696f'
down_revision = 'e8d3b18e360d'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the updated schema
    op.create_table('new_user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),  # Updated length
        sa.Column('role', sa.String(length=50), nullable=False, server_default='Administrator'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO new_user (id, email, password_hash, role) SELECT id, email, password_hash, role FROM user')

    # Drop the old table
    op.drop_table('user')

    # Rename the new table to the original name
    op.rename_table('new_user', 'user')

def downgrade():
    # Create a new table with the original schema
    op.create_table('new_user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=False),  # Original length
        sa.Column('role', sa.String(length=50), nullable=False, server_default='Administrator'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Copy data from the current table to the new table
    op.execute('INSERT INTO new_user (id, email, password_hash, role) SELECT id, email, password_hash, role FROM user')

    # Drop the current table
    op.drop_table('user')

    # Rename the new table to the original name
    op.rename_table('new_user', 'user')