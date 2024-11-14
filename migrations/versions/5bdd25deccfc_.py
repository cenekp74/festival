"""empty message

Revision ID: 5bdd25deccfc
Revises: 63075c566364
Create Date: 2024-11-14 20:51:13.626996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bdd25deccfc'
down_revision = '63075c566364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.add_column(sa.Column('short_description', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('film', schema=None) as batch_op:
        batch_op.drop_column('short_description')

    # ### end Alembic commands ###
