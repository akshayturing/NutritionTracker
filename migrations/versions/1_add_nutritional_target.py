# migrations/versions/xxxx_add_nutritional_targets.py
"""add nutritional targets

Revision ID: xxxx
Revises: previous_revision_id
Create Date: 2023-xx-xx

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '1'
down_revision = 'previous_revision_id'  # Replace with actual previous revision
branch_labels = None
depends_on = None

def upgrade():
    # Add nutritional target columns to users table
    op.add_column('users', sa.Column('calorie_goal', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('protein_goal', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('carbs_goal', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('fat_goal', sa.Integer(), nullable=True))

def downgrade():
    # Remove nutritional target columns from users table
    op.drop_column('users', 'calorie_goal')
    op.drop_column('users', 'protein_goal')
    op.drop_column('users', 'carbs_goal')
    op.drop_column('users', 'fat_goal')