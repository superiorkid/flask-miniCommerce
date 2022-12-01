"""empty message

Revision ID: 814ad26e8b73
Revises: 46e1ab967895
Create Date: 2022-11-30 14:52:09.846490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '814ad26e8b73'
down_revision = '46e1ab967895'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
