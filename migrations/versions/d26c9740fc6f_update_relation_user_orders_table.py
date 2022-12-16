"""update relation User->Orders table

Revision ID: d26c9740fc6f
Revises: 08fd9ac4b641
Create Date: 2022-12-16 17:10:12.004951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd26c9740fc6f'
down_revision = '08fd9ac4b641'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('customer_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['customer_id'], ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_orders_id_fkey', type_='foreignkey')
        batch_op.drop_column('orders_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('orders_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('user_orders_id_fkey', 'orders', ['orders_id'], ['id'])

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('customer_id')

    # ### end Alembic commands ###
