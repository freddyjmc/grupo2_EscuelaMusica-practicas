import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.crud.levels import add_level, get_all_levels, get_level_by_id, update_level, delete_level
from app.utils.app_logging import log_request

# Configuración del logger
logger = logging.getLogger(__name__)

levels_bp = Blueprint('levels', __name__)

@levels_bp.route('/levels', methods=['POST'])
@jwt_required()
@log_request
def create_level():
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} creando nuevo nivel: {data}")
    result = add_level(data)
    if isinstance(result, tuple) and result[1] != 201:
        logger.error(f"Error al crear nivel: {result[0]}")
    else:
        logger.info(f"Nivel creado exitosamente: {result}")
    return result

@levels_bp.route('/levels', methods=['GET'])
@jwt_required()
@log_request
def list_levels():
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando lista de todos los niveles")
    levels = get_all_levels()
    logger.info(f"Se recuperaron {len(levels)} niveles")
    return jsonify(levels)

@levels_bp.route('/levels/<int:id>', methods=['GET'])
@jwt_required()
@log_request
def retrieve_level(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} solicitando detalles del nivel con ID: {id}")
    result = get_level_by_id(id)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al recuperar nivel con ID {id}: {result[0]}")
    else:
        logger.info(f"Nivel con ID {id} recuperado exitosamente")
    return result

@levels_bp.route('/levels/<int:id>', methods=['PUT'])
@jwt_required()
@log_request
def edit_level(id):
    current_user = get_jwt_identity()
    data = request.json
    logger.info(f"Usuario {current_user} intentando actualizar nivel con ID {id}: {data}")
    result = update_level(id, data)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al actualizar nivel con ID {id}: {result[0]}")
    else:
        logger.info(f"Nivel con ID {id} actualizado exitosamente")
    return result

@levels_bp.route('/levels/<int:id>', methods=['DELETE'])
@jwt_required()
@log_request
def remove_level(id):
    current_user = get_jwt_identity()
    logger.info(f"Usuario {current_user} intentando eliminar nivel con ID {id}")
    result = delete_level(id)
    if isinstance(result, tuple) and result[1] != 200:
        logger.error(f"Error al eliminar nivel con ID {id}: {result[0]}")
    else:
        logger.info(f"Nivel con ID {id} eliminado exitosamente")
    return result
