import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.crud.enrollments import add_enrollment, get_all_enrollments, get_enrollment_by_id, update_enrollment, delete_enrollment
from app.utils.app_logging import log_request
from app import db

# Configuración del logger
logger = logging.getLogger(__name__)

enrollments_bp = Blueprint('enrollments', __name__)

@enrollments_bp.route('/enrollments', methods=['POST'])
@jwt_required()
@log_request
def create_enrollment():
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} creando nueva inscripción: {data}")
    result = add_enrollment(data)
    logger.info(f"Resultado de crear inscripción: {result}")
    return result

@enrollments_bp.route('/enrollments', methods=['GET'])
@jwt_required()
@log_request
def list_enrollments():
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando lista de inscripciones")
    enrollments = get_all_enrollments()
    logger.info(f"Retornando {len(enrollments)} inscripciones")
    return jsonify(enrollments)

@enrollments_bp.route('/enrollments/<int:id>', methods=['GET'])
@jwt_required()
@log_request
def retrieve_enrollment(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando inscripción con ID: {id}")
    result = get_enrollment_by_id(id)
    logger.info(f"Resultado de obtener inscripción {id}: {result}")
    return result

@enrollments_bp.route('/enrollments/<int:id>', methods=['PUT'])
@jwt_required()
@log_request
def edit_enrollment(id):
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} actualizando inscripción {id}: {data}")
    result = update_enrollment(id, data)
    logger.info(f"Resultado de actualizar inscripción {id}: {result}")
    return result

@enrollments_bp.route('/enrollments/<int:id>', methods=['DELETE'])
@jwt_required()
@log_request
def remove_enrollment(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} eliminando inscripción {id}")
    result = delete_enrollment(id)
    logger.info(f"Resultado de eliminar inscripción {id}: {result}")
    return result
