import logging
from app.models import Level
from app.schemas import level_schema, levels_schema
from app import db

# Configura el nivel de registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_level(data):
    try:
        new_level = Level(**data)
        db.session.add(new_level)
        db.session.commit()
        logging.info(f"Nivel agregado: {new_level}")
        return level_schema.jsonify(new_level)
    except Exception as e:
        logging.error(f"Error al agregar nivel: {e}")
        return "Error adding level", 500

def get_all_levels():
    try:
        levels = Level.query.all()
        logging.info(f"Se obtuvieron {len(levels)} niveles")
        return levels_schema.dump(levels)
    except Exception as e:
        logging.error(f"Error al obtener niveles: {e}")
        return "Error fetching levels", 500

def get_level_by_id(level_id):
    try:
        level = Level.query.get_or_404(level_id)
        logging.info(f"Se obtuvo el nivel: {level}")
        return level_schema.jsonify(level)
    except Exception as e:
        logging.error(f"Error al obtener el nivel por ID: {e}")
        return "Error fetching level", 404

def update_level(level_id, data):
    try:
        level = Level.query.get_or_404(level_id)
        for key, value in data.items():
            setattr(level, key, value)
        db.session.commit()
        logging.info(f"Nivel actualizado: {level}")
        return level_schema.jsonify(level)
    except Exception as e:
        logging.error(f"Error al actualizar el nivel: {e}")
        return "Error updating level", 500

def delete_level(level_id):
    try:
        level = Level.query.get_or_404(level_id)
        db.session.delete(level)
        db.session.commit()
        logging.info(f"Nivel eliminado: {level}")
        return level_schema.jsonify(level)
    except Exception as e:
        logging.error(f"Error al eliminar el nivel: {e}")
        return "Error deleting level", 500
