"""First migration

Revision ID: 30c01d357944
Revises: 
Create Date: 2021-10-26 20:13:11.793526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30c01d357944'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_url', sa.Text(), nullable=True),
    sa.Column('shorten_url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url')
    # ### end Alembic commands ###
