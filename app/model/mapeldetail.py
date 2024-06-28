from app import db

class MapelDetail(db.Model):
    __tablename__ = 'detail_mapel'
    id = db.Column(db.Integer, primary_key=True)
    nama_mapel = db.Column(db.String(100), nullable=False)
    deskripsi_mapel = db.Column(db.String(255))
    topik_mapel = db.Column(db.String(100))
    image = db.Column(db.String(100))


    def __repr__(self):
        return '<MapelDetail {}>'.format(self.nama_mapel)


