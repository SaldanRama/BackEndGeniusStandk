from app.model.guru import Guru
from app import response, db
from flask import request
import logging


# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def index():
    try:
        guru = Guru.query.all()
        data = formatarray(guru)
        logger.debug(f"Formatted data: {data}")
        return response.success(data, "success")
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return response.error([], "Failed to fetch data")

def formatarray(datas):
    array = []
    for i in datas:
        array.append(singelObject(i))
    return array

def singelObject(data):
    return {
        'id_guru': data.id_guru,
        'nama_guru': data.nama_guru,
        'bidang_studi': data.bidang_studi,
        'pengalaman_mengajar': data.pengalaman_mengajar,
        'email': data.email
    }

def save():
    try:
        nama_guru = request.form.get('nama_guru')
        bidang_studi = request.form.get('bidang_studi')
        pengalaman_mengajar = request.form.get('pengalaman_mengajar')
        email = request.form.get('email')

        logger.debug(f"Data received: nama_guru={nama_guru}, bidang_studi={bidang_studi}, pengalaman_mengajar={pengalaman_mengajar}, email={email}")

        guru = Guru(nama_guru=nama_guru, bidang_studi=bidang_studi, pengalaman_mengajar=pengalaman_mengajar, email=email)
        db.session.add(guru)
        db.session.commit()

        return response.success('', 'Sukses menambahkan data guru')
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return response.error([], 'Failed to add data')

def get_by_id(id):
    try:
        guru = Guru.query.filter_by(id_guru=id).first()
        if not guru:
            logger.error(f'Guru with id {id} not found')
            return response.error([], f'Guru with id {id} not found')

        data = singelObject(guru)
        return response.success(data, 'Success')
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return response.error([], 'Failed to fetch data')

def update(id):
    try:
        guru = Guru.query.filter_by(id_guru=id).first()
        if not guru:
            logger.error(f'Guru with id {id} not found')
            return response.error([], f'Guru with id {id} not found')

        nama_guru = request.form.get('nama_guru')
        bidang_studi = request.form.get('bidang_studi')
        pengalaman_mengajar = request.form.get('pengalaman_mengajar')
        email = request.form.get('email')

        logger.debug(f"Updating guru {id}: nama_guru={nama_guru}, bidang_studi={bidang_studi}, pengalaman_mengajar={pengalaman_mengajar}, email={email}")

        if nama_guru:
            guru.nama_guru = nama_guru
        if bidang_studi:
            guru.bidang_studi = bidang_studi
        if pengalaman_mengajar:
            guru.pengalaman_mengajar = pengalaman_mengajar
        if email:
            guru.email = email

        db.session.commit()

        return response.success(singelObject(guru), 'Data guru berhasil diperbarui')
    except Exception as e:
        logger.error(f"Error updating data: {e}")
        return response.error([], 'Failed to update data')

def delete(id):
    try:
        guru = Guru.query.filter_by(id_guru=id).first()
        if not guru:
            logger.error(f'Guru with id {id} not found')
            return response.error([], f'Guru with id {id} not found')

        db.session.delete(guru)
        db.session.commit()
        return response.success('', 'Data guru berhasil dihapus')
    except Exception as e:
        logger.error(f"Error deleting data: {e}")
        return response.error([], 'Failed to delete data')
