from werkzeug.security import generate_password_hash as werkzeug_generate_password_hash
from werkzeug.security import check_password_hash as werkzeug_check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from datetime import timedelta

def generate_password_hash(password):
    """
    Genera un hash seguro para la contraseña proporcionada.
    
    :param password: La contraseña en texto plano
    :return: Hash de la contraseña
    """
    return werkzeug_generate_password_hash(password)

def check_password_hash(pwhash, password):
    """
    Verifica si una contraseña coincide con un hash dado.
    
    :param pwhash: El hash de la contraseña almacenada
    :param password: La contraseña en texto plano a verificar
    :return: True si la contraseña coincide, False en caso contrario
    """
    return werkzeug_check_password_hash(pwhash, password)

def generate_tokens(identity):
    """
    Genera tokens de acceso y refresco para un usuario.
    
    :param identity: Identificador único del usuario (por ejemplo, id o username)
    :return: Diccionario con los tokens de acceso y refresco
    """
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

def get_current_user_identity():
    """
    Obtiene la identidad del usuario actual a partir del token JWT.
    
    :return: Identidad del usuario actual
    """
    return get_jwt_identity()