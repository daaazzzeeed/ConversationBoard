"""

Revision ID: cff8c2e1030d
Revises: 8733178adf82
Create Date: 2022-09-05 20:01:56.427782

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cff8c2e1030d'
down_revision = '8733178adf82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('related_post_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'post', ['related_post_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'related_post_id')
    # ### end Alembic commands ###
