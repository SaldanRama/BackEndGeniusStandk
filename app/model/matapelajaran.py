from app import db

class MataPelajaran(db.Model):
    __tablename__ = 'data_matapelajaran'
    id_mata_pelajaran = db.Column(db.Integer, primary_key=True)
    nama_mata_pelajaran = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.String(255))
    topik = db.Column(db.String(100))
    materi = db.Column(db.String(100))
    link_video = db.Column(db.String(100))


    def __repr__(self):
        return '<Matapelajaran {}>'.format(self.nama_mata_pelajaran)
