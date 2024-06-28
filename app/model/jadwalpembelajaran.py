from app import db
from app.model.kelas import Kelas
from app.model.guru import Guru
from app.model.matapelajaran import MataPelajaran

class JadwalPelajaran(db.Model):
    __tablename__ = 'data_jadwalpelajaran'
    id_jadwal = db.Column(db.Integer, primary_key=True)
    id_kelas = db.Column(db.Integer, db.ForeignKey('data_kelas.id_kelas'))
    id_guru = db.Column(db.Integer, db.ForeignKey('data_guru.id_guru'))
    id_mata_pelajaran = db.Column(db.Integer, db.ForeignKey('data_matapelajaran.id_mata_pelajaran'))
    hari = db.Column(db.String(20))
    jam_mulai = db.Column(db.Time)
    jam_selesai = db.Column(db.Time)

    def __repr__(self):
        return '<Jadwalpembelajaran {}>'.format(self.name)