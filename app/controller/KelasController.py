import logging
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from app import db, app
from app.model.kelas import Kelas
import os
from werkzeug.utils import secure_filename
from datetime import datetime

kelas_bp = Blueprint('kelas', __name__)

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    logging.debug(f"Upload folder ensured at {UPLOAD_FOLDER}")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fungsi untuk menghasilkan nama file yang unik dengan prefix
def generate_unique_filename(prefix, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extension = filename.split('.')[-1]
    new_filename = f"{prefix}_{timestamp}.{extension}"
    return new_filename

@kelas_bp.route('/upload', methods=['POST'])
def upload_file():
    ensure_upload_folder()  # Pastikan folder upload ada
    logging.debug("Upload folder ensured.")
    if 'photo' not in request.files:
        logging.error("No file part in request.")
        return jsonify({"error": "No file part"}), 400
    file = request.files['photo']
    if file.filename == '':
        logging.error("No selected file.")
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = generate_unique_filename('photo', secure_filename(file.filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        logging.debug(f"File {filename} successfully uploaded.")
        return jsonify({"message": "File successfully uploaded", "filename": filename}), 200
    else:
        logging.error("File type not allowed.")
        return jsonify({"error": "File type not allowed"}), 400

@kelas_bp.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    try:
        logging.debug(f"Attempting to send file from path: {os.path.join(current_app.config['UPLOAD_FOLDER'], filename)}")
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        return jsonify({"error": "File not found"}), 404

@kelas_bp.route('/list_uploads', methods=['GET'])
def list_uploads():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    logging.debug(f"Files in upload folder: {files}")
    return jsonify(files)

# Create
@kelas_bp.route('/kelas', methods=['POST'])
def create_kelas():
    ensure_upload_folder()  # Pastikan folder upload ada
    if 'image' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = generate_unique_filename('kelas', secure_filename(file.filename))
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        new_kelas = Kelas(
            nama_kelas=request.form['nama_kelas'],
            deskripsi_mapel=request.form.get('deskripsi_mapel'),
            topik_mapel=request.form.get('topik_mapel'),
            image=filename
        )
        db.session.add(new_kelas)
        db.session.commit()
        return jsonify({'message': 'Kelas created successfully'}), 201
    else:
        return jsonify({'message': 'File type not allowed'}), 415

# Update
@kelas_bp.route('/kelas/<id>', methods=['PUT'])
def update_kelas(id):
    kelas = Kelas.query.get(id)
    if not kelas:
        return jsonify({'message': 'Kelas not found'}), 404

    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = generate_unique_filename('kelas', secure_filename(file.filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            kelas.image = filename
        else:
            return jsonify({'message': 'File type not allowed'}), 415

    kelas.nama_kelas = request.form['nama_kelas']
    kelas.deskripsi_mapel = request.form.get('deskripsi_mapel')
    kelas.topik_mapel = request.form.get('topik_mapel')
    db.session.commit()
    return jsonify({'message': 'Kelas updated successfully'}), 200

# Read
@kelas_bp.route('/kelas', methods=['GET'])
def get_all_kelas():
    kelas_list = Kelas.query.all()
    result = []
    for kelas in kelas_list:
        kelas_data = {
            'id_kelas': kelas.id_kelas,
            'nama_kelas': kelas.nama_kelas,
            'deskripsi_mapel': kelas.deskripsi_mapel,
            'topik_mapel': kelas.topik_mapel,
            'image': f"/uploads/{kelas.image}"  # Pastikan path file gambar benar
        }
        result.append(kelas_data)
    return jsonify(result), 200

@kelas_bp.route('/kelas/nama', methods=['GET'])
def get_all_kelas_nama():
    kelas_list = Kelas.query.with_entities(Kelas.nama_kelas).all()
    result = [kelas.nama_kelas for kelas in kelas_list]
    return jsonify(result), 200

@kelas_bp.route('/kelas/<id>', methods=['GET'])
def get_kelas(id):
    kelas = Kelas.query.get(id)
    if not kelas:
        return jsonify({'message': 'Kelas not found'}), 404
    kelas_data = {
        'id_kelas': kelas.id_kelas,
        'nama_kelas': kelas.nama_kelas,
        'deskripsi_mapel': kelas.deskripsi_mapel,
        'topik_mapel': kelas.topik_mapel,
        'image': f"/uploads/{kelas.image}"  # Pastikan path file gambar benar
    }
    return jsonify(kelas_data), 200

# Delete
@kelas_bp.route('/kelas/<id>', methods=['DELETE'])
def delete_kelas(id):
    kelas = Kelas.query.get(id)
    if not kelas:
        return jsonify({'message': 'Kelas not found'}), 404
    db.session.delete(kelas)
    db.session.commit()
    return jsonify({'message': 'Kelas deleted successfully'}), 200
