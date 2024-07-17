import os
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
from flask import request, g, current_app, make_response
import time

def setup_logger(app):
    """Configura el logger global y de la aplicación."""
    if not app.debug or app.testing:
        log_dir = os.path.join(app.root_path, 'logs')
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
                print(f"Carpeta 'logs' creada en: {log_dir}")
            except Exception as e:
                print(f"No se pudo crear la carpeta 'logs': {e}")
        log_file = os.path.join(log_dir, 'app.log')
        
        file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Evitar agregar múltiples veces el manejador
        if not app.logger.handlers:
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Inicialización del logger')

def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()

        current_app.logger.info(f"Solicitud recibida: {request.method} {request.url}")
        current_app.logger.info(f"Headers: {dict(request.headers)}")
        current_app.logger.info(f"Datos: {request.get_data()}")

        response = f(*args, **kwargs)
        
        # Asegurarse de que `response` sea un objeto de respuesta de Flask
        response = make_response(response)

        duration = time.time() - start_time

        current_app.logger.info(f"Respuesta enviada: {response.status_code}")
        current_app.logger.info(f"Tiempo de respuesta: {duration:.2f} segundos")

        return response
    return decorated_function

def log_error(error):
    """Función para loguear errores."""
    current_app.logger.error(f"Error: {str(error)}", exc_info=True)

def log_info(message):
    """Función para loguear información general."""
    current_app.logger.info(message)

def log_warning(message):
    """Función para loguear advertencias."""
    current_app.logger.warning(message)

def log_debug(message):
    """Función para loguear mensajes de debug."""
    current_app.logger.debug(message)
