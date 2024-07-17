import logging
from app.models import Instrument
from app.schemas import instrument_schema, instruments_schema
from app import db

# Configura el nivel de registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_instrument(data):
    try:
        new_instrument = Instrument(**data)
        db.session.add(new_instrument)
        db.session.commit()
        logging.info(f"Instrumento agregado: {new_instrument}")
        return instrument_schema.jsonify(new_instrument)
    except Exception as e:
        logging.error(f"Error al agregar instrumento: {e}")
        return "Error adding instrument", 500

def get_all_instruments():
    try:
        instruments = Instrument.query.all()
        logging.info(f"Se obtuvieron {len(instruments)} instrumentos")
        return instruments_schema.dump(instruments)
    except Exception as e:
        logging.error(f"Error al obtener instrumentos: {e}")
        return "Error fetching instruments", 500

def get_instrument_by_id(instrument_id):
    try:
        instrument = Instrument.query.get_or_404(instrument_id)
        logging.info(f"Se obtuvo el instrumento: {instrument}")
        return instrument_schema.jsonify(instrument)
    except Exception as e:
        logging.error(f"Error al obtener el instrumento por ID: {e}")
        return "Error fetching instrument", 404

def update_instrument(instrument_id, data):
    try:
        instrument = Instrument.query.get_or_404(instrument_id)
        for key, value in data.items():
            setattr(instrument, key, value)
        db.session.commit()
        logging.info(f"Instrumento actualizado: {instrument}")
        return instrument_schema.jsonify(instrument)
    except Exception as e:
        logging.error(f"Error al actualizar el instrumento: {e}")
        return "Error updating instrument", 500

def delete_instrument(instrument_id):
    try:
        instrument = Instrument.query.get_or_404(instrument_id)
        db.session.delete(instrument)
        db.session.commit()
        logging.info(f"Instrumento eliminado: {instrument}")
        return instrument_schema.jsonify(instrument)
    except Exception as e:
        logging.error(f"Error al eliminar el instrumento: {e}")
        return "Error deleting instrument", 500
