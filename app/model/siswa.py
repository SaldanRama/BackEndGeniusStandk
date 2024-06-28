from app import db

class Siswa(db.Model):
    __tablename__ = 'data_siswa'
    id_siswa = db.Column(db.Integer, primary_key=True)
    nama_siswa = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(100))
    no_telepon = db.Column(db.String(15))
    email = db.Column(db.String(100))
    kelas = db.Column(db.String(10))

    
    def __repr__(self):
        return '<Siswa {}>'.format(self.name)