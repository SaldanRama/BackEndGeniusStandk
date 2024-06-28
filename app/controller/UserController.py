from flask import Flask, request, jsonify
from flask_cors import CORS
from app.model.user import User
from app import response, db
from datetime import datetime, timedelta
import logging
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def buatAdmin():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')  # Nama Lengkap
        birth_date = data.get('birth_date')  # Tanggal Lahir
        class_name = data.get('class_name')  # Kelas
        phone_number = data.get('phone_number')  # Nomor HP
        domicile = data.get('domicile')  # Domisili
        level = 1

        logger.debug(f"Received data - Name: {name}, Email: {email}, Password: {password}, Level: {level}, Full Name: {full_name}, Birth Date: {birth_date}, Class: {class_name}, Phone Number: {phone_number}, Domicile: {domicile}")

        if not all([name, email, password]):
            raise ValueError("All fields are required: name, email, password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError("User with this email already exists")

        logger.debug("No existing user found, proceeding to create a new user")

        user = User(
            name=name, 
            email=email, 
            level=level, 
            full_name=full_name, 
            birth_date=birth_date, 
            class_name=class_name, 
            phone_number=phone_number, 
            domicile=domicile
        )
        user.setPassword(password)

        logger.debug(f"User object before saving: {user}")

        db.session.add(user)
        db.session.commit()

        logger.debug("User successfully added to the database")

        return response.success('', 'Selamat Kamu Berhasil Registrasi!!')
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return response.error([], str(e))
    finally:
        db.session.close()

def singleObject(data):
    return {
        'id': data.id,
        'name': data.name,
        'email': data.email,
        'level': data.level,
        'full_name': data.full_name,  # Nama Lengkap
        'birth_date': data.birth_date,  # Tanggal Lahir
        'class_name': data.class_name,  # Kelas
        'phone_number': data.phone_number,  # Nomor HP
        'domicile': data.domicile  # Domisili
    }

def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        logger.debug(f"Login attempt - Email: {email}, Password: {password}")

        user = User.query.filter_by(email=email).first()

        if not user:
            logger.error(f"Email {email} not registered")
            return response.badRequest([], 'Email tidak terdaftar')
        
        if not user.checkPassword(password):
            logger.error("Incorrect password")
            return response.badRequest([], 'Password Salah')
        
        user_data = singleObject(user)

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        access_token = create_access_token(identity=user_data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=user_data, expires_delta=expires_refresh)

        logger.debug("Login successful, tokens generated")

        return response.success({
            "data": user_data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, "Sukses Login!")
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return response.error([], 'Failed to login')

def delete_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            logger.error(f'User with id {user_id} not found')
            return response.error([], f'User with id {user_id} not found')

        db.session.delete(user)
        db.session.commit()
        return response.success('', 'User deleted successfully')
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return response.error([], 'Failed to delete user')

def get_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            logger.error(f'User with id {user_id} not found')
            return response.error([], f'User with id {user_id} not found')

        user_data = singleObject(user)
        return response.success(user_data, 'Success')
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return response.error([], 'Failed to fetch user')

def update_user(user_id):
    try:
        data = request.json
        user = User.query.filter_by(id=user_id).first()

        if not user:
            # Jika pengguna tidak ditemukan, buat pengguna baru
            user = User(
                id=user_id,
                name=data.get('name'),
                email=data.get('email'),
                full_name=data.get('full_name'),  # Nama Lengkap
                birth_date=data.get('birth_date'),  # Tanggal Lahir
                class_name=data.get('class_name'),  # Kelas
                phone_number=data.get('phone_number'),  # Nomor HP
                domicile=data.get('domicile')  # Domisili
            )
            if 'password' in data:
                user.setPassword(data['password'])
            db.session.add(user)
            logger.debug(f"User with id {user_id} created")
        else:
            # Jika pengguna ditemukan, perbarui data yang ada
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.full_name = data.get('full_name', user.full_name)  # Nama Lengkap
            user.birth_date = data.get('birth_date', user.birth_date)  # Tanggal Lahir
            user.class_name = data.get('class_name', user.class_name)  # Kelas
            user.phone_number = data.get('phone_number', user.phone_number)  # Nomor HP
            user.domicile = data.get('domicile', user.domicile)  # Domisili

            if 'password' in data:
                user.setPassword(data['password'])

            logger.debug(f"User with id {user_id} updated")

        db.session.commit()

        return response.success('', 'User updated successfully')
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return response.error([], 'Failed to update user')