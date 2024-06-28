from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250),nullable=False)
    email = db.Column(db.String(60),index=True, unique=True, nullable=False)
    password = db.Column(db.String(250),nullable=False)
    level = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    full_name = db.Column(db.String(250), nullable=True)  # Nama Lengkap
    birth_date = db.Column(db.Date, nullable=True)  # Tanggal Lahir
    class_name = db.Column(db.String(100), nullable=True)  # Kelas
    phone_number = db.Column(db.String(20), nullable=True)  # Nomor HP
    domicile = db.Column(db.String(250), nullable=True)  # Domisili

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
