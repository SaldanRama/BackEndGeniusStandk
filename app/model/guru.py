from app import db

class Guru(db.Model):
    __tablename__ = 'data_guru'
    id_guru = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_guru = db.Column(db.String(100), nullable=False)
    bidang_studi = db.Column(db.String(100))
    pengalaman_mengajar = db.Column(db.String(100))

    def __repr__(self):
        return f'<Guru {self.nama_guru}>'
