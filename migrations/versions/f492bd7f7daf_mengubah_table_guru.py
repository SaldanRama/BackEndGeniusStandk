"""mengubah table guru

Revision ID: f492bd7f7daf
Revises: 1104bf7d49d2
Create Date: 2024-06-07 09:06:28.942982

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f492bd7f7daf'
down_revision = '1104bf7d49d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_guru', schema=None) as batch_op:
        batch_op.alter_column('pengalaman_mengajar',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_guru', schema=None) as batch_op:
        batch_op.alter_column('pengalaman_mengajar',
               existing_type=sa.String(length=100),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=True)

    # ### end Alembic commands ###
