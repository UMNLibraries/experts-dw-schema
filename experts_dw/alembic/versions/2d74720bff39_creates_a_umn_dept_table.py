"""Creates a umn_dept table.

Revision ID: 2d74720bff39
Revises: 1e930c89445b
Create Date: 2017-12-13 21:03:49.980958

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '2d74720bff39'
down_revision = '1e930c89445b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('umn_dept',
    sa.Column('deptid', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('deptid', 'timestamp')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('umn_dept')
    # ### end Alembic commands ###
