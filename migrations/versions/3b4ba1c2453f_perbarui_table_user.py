"""perbarui table user

Revision ID: 3b4ba1c2453f
Revises: 6300dd5a2420
Create Date: 2024-06-27 16:03:36.643600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b4ba1c2453f'
down_revision = '6300dd5a2420'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('full_name', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('birth_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('class_name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('domicile', sa.String(length=250), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('domicile')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('class_name')
        batch_op.drop_column('birth_date')
        batch_op.drop_column('full_name')

    # ### end Alembic commands ###
