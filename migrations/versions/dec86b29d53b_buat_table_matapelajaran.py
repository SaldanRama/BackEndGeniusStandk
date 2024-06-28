"""buat table matapelajaran

Revision ID: dec86b29d53b
Revises: 526beeb39aef
Create Date: 2024-06-07 08:44:21.059144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dec86b29d53b'
down_revision = '526beeb39aef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_matapelajaran',
    sa.Column('id_mata_pelajaran', sa.Integer(), nullable=False),
    sa.Column('nama_mata_pelajaran', sa.String(length=100), nullable=False),
    sa.Column('deskripsi', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id_mata_pelajaran')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_matapelajaran')
    # ### end Alembic commands ###
