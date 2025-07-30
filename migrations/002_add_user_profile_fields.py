"""Add user profile fields

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    """Add user profile fields to users table"""
    # Add new columns to users table
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    op.add_column('users', sa.Column('restaurant', sa.String(), nullable=True))


def downgrade():
    """Remove user profile fields from users table"""
    # Remove columns from users table
    op.drop_column('users', 'restaurant')
    op.drop_column('users', 'role')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name') 