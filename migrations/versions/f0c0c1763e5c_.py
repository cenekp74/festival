"""empty message

Revision ID: f0c0c1763e5c
Revises: 9e081ca4c58b
Create Date: 2024-12-10 22:15:49.286894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0c0c1763e5c'
down_revision = '9e081ca4c58b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workshop', schema=None) as batch_op:
        batch_op.drop_column('author')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workshop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=50), nullable=True))

    # ### end Alembic commands ###
