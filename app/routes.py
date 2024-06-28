from app import app, db
from app.controller import GuruController
from app.controller import UserController
from app.controller import MapelController
from app.controller.KelasController import kelas_bp
from flask import request, jsonify
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.model import User

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Register KelasController routes
app.register_blueprint(kelas_bp)

@app.route('/')
def index():
    return "Hello World"

@app.route('/guru', methods=['GET', 'POST'])
def gurus():
    if request.method == 'GET':
        return GuruController.index()
    elif request.method == 'POST':
        return GuruController.save()

@app.route('/createadmin', methods=['POST'])
def admins():
    return UserController.buatAdmin()

@app.route('/guru/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_guru(id):
    if request.method == 'GET':
        return GuruController.get_by_id(id)
    elif request.method == 'PUT':
        return GuruController.update(id)
    elif request.method == 'DELETE':
        return GuruController.delete(id)

@app.route('/login', methods=['POST'])
def logins():
    logger.debug(f"Request form data: {request.form}")
    return UserController.login()

@app.route('/current_user', methods=['GET'])
@jwt_required()
def current_user():
    try:
        identity = get_jwt_identity()
        logger.debug(f"JWT Identity: {identity}")
        
        user = User.query.get(identity['id'])
        if not user:
            logger.error("User not found")
            return jsonify({"msg": "User not found"}), 404
        
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "full_name": user.full_name,  # Nama Lengkap
            "birth_date": user.birth_date,  # Tanggal Lahir
            "class_name": user.class_name,  # Kelas
            "phone_number": user.phone_number,  # Nomor HP
            "domicile": user.domicile, # Domisili
            "password" : user. password
        }
        
        logger.debug(f"User data: {user_data}")
        
        return jsonify({"data": user_data}), 200
    except Exception as e:
        logger.error(f"Error fetching current user: {e}")
        return jsonify({"msg": "Internal Server Error"}), 500

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(id):
    if request.method == 'GET':
        return UserController.get_user(id)
    elif request.method == 'PUT':
        return UserController.update_user(id)
    elif request.method == 'DELETE':
        return UserController.delete_user(id)

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({"msg": "No users found"}), 404
    
    users_data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "full_name": user.full_name,  # Nama Lengkap
            "birth_date": user.birth_date,  # Tanggal Lahir
            "class_name": user.class_name,  # Kelas
            "phone_number": user.phone_number,  # Nomor HP
            "domicile": user.domicile  # Domisili
        } for user in users
    ]
    
    return jsonify({
        "data": users_data
    }), 200

@app.route('/mapel', methods=['GET', 'POST'])
def handle_mapel():
    if request.method == 'GET':
        return MapelController.index()
    elif request.method == 'POST':
        return MapelController.save()

@app.route('/mapel/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_mapel_by_id(id):
    if request.method == 'GET':
        return MapelController.get_by_id(id)
    elif request.method == 'PUT':
        return MapelController.update(id)
    elif request.method == 'DELETE':
        return MapelController.delete(id)
