"""add proof of payment table

Revision ID: a356725c1e70
Revises: 39bfa40ed8a3
Create Date: 2023-01-02 14:22:37.380617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a356725c1e70'
down_revision = '39bfa40ed8a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('proof_of_payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('payer', sa.String(length=100), nullable=False),
    sa.Column('payee', sa.String(length=100), nullable=False),
    sa.Column('payment_method', sa.String(length=100), nullable=False),
    sa.Column('proof_of_payment', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('proof_of_payment')
    # ### end Alembic commands ###
