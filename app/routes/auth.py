import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db
from app.utils.app_logging import log_request
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración del logger
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@log_request
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.username)
        logger.info(f"Usuario {user.username} ha iniciado sesión")
        return jsonify(access_token=access_token), 200
    else:
        logger.warning(f"Intento de inicio de sesión fallido para el usuario: {data['username']}")
        return jsonify({"msg": "Invalid username or password"}), 401

@auth_bp.route('/register', methods=['POST'])
@log_request
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"msg": "Missing username or password"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400
    
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    
    try:
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"Usuario creado exitosamente: {new_user.username}")
        return jsonify({"msg": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al crear usuario: {str(e)}")
        return jsonify({"msg": "Failed to create user"}), 500

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
@log_request
def list_users():
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando lista de usuarios")
    
    users = User.query.all()
    user_list = [{"username": user.username, "id": user.id} for user in users]
    
    logger.info(f"Retornando {len(user_list)} usuarios")
    return jsonify(user_list), 200

@auth_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
@log_request
def retrieve_user(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando información del usuario con ID: {id}")
    
    user = User.query.get(id)
    if user:
        user_data = {"username": user.username, "id": user.id}
        logger.info(f"Retornando información del usuario: {user_data}")
        return jsonify(user_data), 200
    else:
        logger.warning(f"No se encontró el usuario con ID: {id}")
        return jsonify({"msg": "User not found"}), 404

@auth_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@log_request
def edit_user(id):
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} actualizando información del usuario con ID: {id}")
    
    user = User.query.get(id)
    if user:
        try:
            if 'username' in data:
                user.username = data['username']
            if 'password' in data:
                user.set_password(data['password'])
            db.session.commit()
            logger.info(f"Usuario actualizado correctamente: {user.username}")
            return jsonify({"msg": "User updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar usuario: {str(e)}")
            return jsonify({"msg": "Failed to update user"}), 500
    else:
        logger.warning(f"No se encontró el usuario con ID: {id}")
        return jsonify({"msg": "User not found"}), 404

@auth_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@log_request
def delete_user(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} eliminando usuario con ID: {id}")
    
    user = User.query.get(id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            logger.info(f"Usuario eliminado correctamente: {user.username}")
            return jsonify({"msg": "User deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar usuario: {str(e)}")
            return jsonify({"msg": "Failed to delete user"}), 500
    else:
        logger.warning(f"No se encontró el usuario con ID: {id}")
        return jsonify({"msg": "User not found"}), 404
