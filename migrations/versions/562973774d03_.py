"""empty message

Revision ID: 562973774d03
Revises: bc04ea900312
Create Date: 2022-11-26 21:38:41.238194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '562973774d03'
down_revision = 'bc04ea900312'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('discounted_price')
        batch_op.drop_column('product_review')
        batch_op.drop_column('product_rating')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_rating', sa.NUMERIC(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('product_review', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('discounted_price', sa.NUMERIC(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###