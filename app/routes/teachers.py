import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.crud.teachers import add_teacher, get_all_teachers, get_teacher_by_id, update_teacher, delete_teacher
from app.utils.app_logging import log_request

# Configuración del logger
logger = logging.getLogger(__name__)

teachers_bp = Blueprint('teachers', __name__)

@teachers_bp.route('/teachers', methods=['POST'])
@jwt_required()
@log_request
def create_teacher():
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} creando nuevo profesor: {data}")
    result = add_teacher(data)
    if isinstance(result, tuple) and result[1] != 201:
        logger.error(f"Error al crear profesor: {result[0]}")
    else:
        logger.info(f"Profesor creado exitosamente: {result}")
    return result

@teachers_bp.route('/teachers', methods=['GET'])
@jwt_required()
@log_request
def list_teachers():
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando lista de todos los profesores")
    teachers = get_all_teachers()
    logger.info(f"Se recuperaron {len(teachers)} profesores")
    return jsonify(teachers)

@teachers_bp.route('/teachers/<int:id>', methods=['GET'])
@jwt_required()
@log_request
def retrieve_teacher(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando detalles del profesor con ID: {id}")
    result = get_teacher_by_id(id)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al recuperar profesor con ID {id}: {result[0]}")
    else:
        logger.info(f"Profesor con ID {id} recuperado exitosamente")
    return result

@teachers_bp.route('/teachers/<int:id>', methods=['PUT'])
@jwt_required()
@log_request
def edit_teacher(id):
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} intentando actualizar profesor con ID {id}: {data}")
    result = update_teacher(id, data)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al actualizar profesor con ID {id}: {result[0]}")
    else:
        logger.info(f"Profesor con ID {id} actualizado exitosamente")
    return result

@teachers_bp.route('/teachers/<int:id>', methods=['DELETE'])
@jwt_required()
@log_request
def remove_teacher(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} intentando eliminar profesor con ID {id}")
    result = delete_teacher(id)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al eliminar profesor con ID {id}: {result[0]}")
    else:
        logger.info(f"Profesor con ID {id} eliminado exitosamente")
    return result
