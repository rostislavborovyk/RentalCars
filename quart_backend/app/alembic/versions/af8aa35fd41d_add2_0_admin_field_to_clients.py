"""Add2.0 admin field to clients

Revision ID: af8aa35fd41d
Revises: 4f427030933a
Create Date: 2020-07-02 15:16:22.294075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af8aa35fd41d'
down_revision = '4f427030933a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clients', sa.Column('admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clients', 'admin')
    # ### end Alembic commands ###
