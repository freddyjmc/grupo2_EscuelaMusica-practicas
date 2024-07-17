import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.crud.students import add_student, get_all_students, get_student_by_id, update_student, delete_student
from app.utils.app_logging import log_request

# Configuración del logger
logger = logging.getLogger(__name__)

students_bp = Blueprint('students', __name__)

@students_bp.route('/students', methods=['POST'])
@jwt_required()
@log_request
def create_student():
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} creando nuevo estudiante: {data}")
    result = add_student(data)
    if isinstance(result, tuple) and result[1] != 201:
        logger.error(f"Error al crear estudiante: {result[0]}")
    else:
        logger.info(f"Estudiante creado exitosamente: {result}")
    return result

@students_bp.route('/students', methods=['GET'])
@jwt_required()
@log_request
def list_students():
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando lista de todos los estudiantes")
    students = get_all_students()
    logger.info(f"Se recuperaron {len(students)} estudiantes")
    return jsonify(students)

@students_bp.route('/students/<int:id>', methods=['GET'])
@jwt_required()
@log_request
def retrieve_student(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando detalles del estudiante con ID: {id}")
    result = get_student_by_id(id)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al recuperar estudiante con ID {id}: {result[0]}")
    else:
        logger.info(f"Estudiante con ID {id} recuperado exitosamente")
    return result

@students_bp.route('/students/<int:id>', methods=['PUT'])
@jwt_required()
@log_request
def edit_student(id):
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} intentando actualizar estudiante con ID {id}: {data}")
    result = update_student(id, data)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al actualizar estudiante con ID {id}: {result[0]}")
    else:
        logger.info(f"Estudiante con ID {id} actualizado exitosamente")
    return result

@students_bp.route('/students/<int:id>', methods=['DELETE'])
@jwt_required()
@log_request
def remove_student(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} intentando eliminar estudiante con ID {id}")
    result = delete_student(id)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al eliminar estudiante con ID {id}: {result[0]}")
    else:
        logger.info(f"Estudiante con ID {id} eliminado exitosamente")
    return result
