from app import db

class TopikMapel(db.Model):
    __tablename__ = 'topik_mapel'
    id = db.Column(db.Integer, primary_key=True)
    nama_topik = db.Column(db.String(100), nullable=False)
    kelas_id = db.Column(db.Integer, db.ForeignKey('kelas.id_kelas'), nullable=False)
    kelas = db.relationship('Kelas', back_populates='topik_mapel')


    def __repr__(self):
        return '<TopikMapel {}>'.format(self.name)