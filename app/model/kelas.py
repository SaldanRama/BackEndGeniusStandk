from app import db

class Kelas(db.Model):
    __tablename__ = 'data_kelas'
    id_kelas = db.Column(db.Integer, primary_key=True)
    nama_kelas = db.Column(db.String(50), nullable=False)
    deskripsi_mapel = db.Column(db.String(255))
    topik_mapel = db.Column(db.String(100))
    image = db.Column(db.String(100))

       
    def __repr__(self):
        return '<Kelas {}>'.format(self.name)