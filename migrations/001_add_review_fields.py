"""Add review and import fields to recipes table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to recipes table
    op.add_column('recipes', sa.Column('review_status', sa.String(), nullable=True, server_default='pending'))
    op.add_column('recipes', sa.Column('imported_at', sa.DateTime(), nullable=True))
    op.add_column('recipes', sa.Column('reviewed_at', sa.DateTime(), nullable=True))
    op.add_column('recipes', sa.Column('reviewed_by', sa.Integer(), nullable=True))
    op.add_column('recipes', sa.Column('source', sa.String(), nullable=True))
    
    # Add foreign key constraint for reviewed_by
    op.create_foreign_key('fk_recipes_reviewed_by', 'recipes', 'users', ['reviewed_by'], ['id'])

def downgrade():
    # Drop foreign key constraint
    op.drop_constraint('fk_recipes_reviewed_by', 'recipes', type_='foreignkey')
    
    # Drop columns
    op.drop_column('recipes', 'source')
    op.drop_column('recipes', 'reviewed_by')
    op.drop_column('recipes', 'reviewed_at')
    op.drop_column('recipes', 'imported_at')
    op.drop_column('recipes', 'review_status') 