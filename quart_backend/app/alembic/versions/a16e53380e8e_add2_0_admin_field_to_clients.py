"""Add2.0 admin field to clients

Revision ID: a16e53380e8e
Revises: 966b0668b160
Create Date: 2020-07-02 16:07:10.195849

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a16e53380e8e'
down_revision = '966b0668b160'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('clients', 'last_name',
               existing_type=mysql.VARCHAR(length=60),
               nullable=True)
    op.create_unique_constraint(None, 'clients', ['passport_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'clients', type_='unique')
    op.alter_column('clients', 'last_name',
               existing_type=mysql.VARCHAR(length=60),
               nullable=False)
    # ### end Alembic commands ###
