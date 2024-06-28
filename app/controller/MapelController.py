from app.model.matapelajaran import MataPelajaran
from app import response, db, app
from flask import request, jsonify
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def index():
    try:
        matapelajaran = MataPelajaran.query.all()
        data = formatarray(matapelajaran)
        logger.debug(f"Formatted data: {data}")
        return response.success(data, "success")
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return response.error([], "Failed to fetch data")

def formatarray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array

def singleObject(data):
    return {
        'id_mata_pelajaran': data.id_mata_pelajaran,
        'nama_mata_pelajaran': data.nama_mata_pelajaran,
        'deskripsi': data.deskripsi,
        'topik': data.topik,
        'materi': data.materi,
        'link_video': data.link_video
    }

def save():
    try:
        data = request.get_json()  # Mengharapkan data JSON
        nama_mata_pelajaran = data.get('nama_mata_pelajaran')
        deskripsi = data.get('deskripsi')
        topik = data.get('topik')
        materi = data.get('materi')
        link_video = data.get('link_video')

        logger.debug(f"Data received: nama_mata_pelajaran={nama_mata_pelajaran}, deskripsi={deskripsi}, topik={topik}, materi={materi}, link_video={link_video}")

        matapelajaran = MataPelajaran(
            nama_mata_pelajaran=nama_mata_pelajaran,
            deskripsi=deskripsi,
            topik=topik,
            materi=materi,
            link_video=link_video
        )
        db.session.add(matapelajaran)
        db.session.commit()

        return response.success('', 'Sukses menambahkan data mata pelajaran')
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return response.error([], 'Failed to add data')

def get_by_id(id):
    try:
        matapelajaran = MataPelajaran.query.filter_by(id_mata_pelajaran=id).first()
        if not matapelajaran:
            logger.error(f'Mata pelajaran with id {id} not found')
            return response.error([], f'Mata pelajaran with id {id} not found')

        data = singleObject(matapelajaran)
        return response.success(data, 'Success')
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return response.error([], 'Failed to fetch data')

def update(id):
    try:
        matapelajaran = MataPelajaran.query.filter_by(id_mata_pelajaran=id).first()
        if not matapelajaran:
            logger.error(f'Mata pelajaran with id {id} not found')
            return response.error([], f'Mata pelajaran with id {id} not found')

        data = request.get_json()
        if not data:
            logger.error('No data provided')
            return response.error([], 'No data provided')

        nama_mata_pelajaran = data.get('nama_mata_pelajaran')
        deskripsi = data.get('deskripsi')
        topik = data.get('topik')
        materi = data.get('materi')
        link_video = data.get('link_video')

        logger.debug(f"Updating mata pelajaran {id}: nama_mata_pelajaran={nama_mata_pelajaran}, deskripsi={deskripsi}, topik={topik}, materi={materi}, link_video={link_video}")

        if nama_mata_pelajaran:
            matapelajaran.nama_mata_pelajaran = nama_mata_pelajaran
        if deskripsi:
            matapelajaran.deskripsi = deskripsi
        if topik:
            matapelajaran.topik = topik
        if materi:
            matapelajaran.materi = materi
        if link_video:
            matapelajaran.link_video = link_video

        db.session.commit()
        return response.success('', 'Sukses memperbarui data mata pelajaran')
    except Exception as e:
        logger.error(f"Error updating data: {e}", exc_info=True)
        return response.error([], 'Failed to update data')

def delete(id):
    try:
        matapelajaran = MataPelajaran.query.filter_by(id_mata_pelajaran=id).first()
        if not matapelajaran:
            return jsonify({"msg": "Mata pelajaran not found"}), 404
        
        db.session.delete(matapelajaran)
        db.session.commit()
        
        logger.debug(f"Successfully deleted mata pelajaran with id: {id}")
        return jsonify({"msg": "Mata pelajaran deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting data: {e}")
        return jsonify({"msg": "Failed to delete data"}), 500

        # Tambahkan endpoint ini di KelasController.py atau file Flask lainnya
