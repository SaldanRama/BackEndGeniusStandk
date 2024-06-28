# app/response.py
from flask import jsonify

def success(values, message):
    res = {
        'status': 'success',
        'message': message,
        'data': values,
    }
    return jsonify(res), 200

def error(values, message):
    res = {
        'status': 'error',
        'message': message,
        'data': values,
    }
    return jsonify(res), 400

def badRequest(values, message):
    res = {
        'status': 'fail',
        'message': message,
        'data': values,
    }
    return jsonify(res), 400
