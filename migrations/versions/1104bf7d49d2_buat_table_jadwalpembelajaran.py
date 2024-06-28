"""buat table Jadwalpembelajaran

Revision ID: 1104bf7d49d2
Revises: dec86b29d53b
Create Date: 2024-06-07 08:53:51.019165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1104bf7d49d2'
down_revision = 'dec86b29d53b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_jadwalpelajaran',
    sa.Column('id_jadwal', sa.Integer(), nullable=False),
    sa.Column('id_kelas', sa.Integer(), nullable=True),
    sa.Column('id_guru', sa.Integer(), nullable=True),
    sa.Column('id_mata_pelajaran', sa.Integer(), nullable=True),
    sa.Column('hari', sa.String(length=20), nullable=True),
    sa.Column('jam_mulai', sa.Time(), nullable=True),
    sa.Column('jam_selesai', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['id_guru'], ['data_guru.id_guru'], ),
    sa.ForeignKeyConstraint(['id_kelas'], ['data_kelas.id_kelas'], ),
    sa.ForeignKeyConstraint(['id_mata_pelajaran'], ['data_matapelajaran.id_mata_pelajaran'], ),
    sa.PrimaryKeyConstraint('id_jadwal')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('data_jadwalpelajaran')
    # ### end Alembic commands ###
