import logging
from app.models import Enrollment
from app.schemas import enrollment_schema, enrollments_schema
from app import db

# Configura el nivel de registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_enrollment(data):
    try:
        new_enrollment = Enrollment(**data)
        db.session.add(new_enrollment)
        db.session.commit()
        logging.info(f"Matrícula agregada: {new_enrollment}")
        return enrollment_schema.jsonify(new_enrollment)
    except Exception as e:
        logging.error(f"Error al agregar matrícula: {e}")
        return "Error adding enrollment", 500

def get_all_enrollments():
    try:
        enrollments = Enrollment.query.all()
        logging.info(f"Se obtuvieron {len(enrollments)} matrículas")
        return enrollments_schema.dump(enrollments)
    except Exception as e:
        logging.error(f"Error al obtener matrículas: {e}")
        return "Error fetching enrollments", 500

def get_enrollment_by_id(enrollment_id):
    try:
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        logging.info(f"Se obtuvo la matrícula: {enrollment}")
        return enrollment_schema.jsonify(enrollment)
    except Exception as e:
        logging.error(f"Error al obtener la matrícula por ID: {e}")
        return "Error fetching enrollment", 404

def update_enrollment(enrollment_id, data):
    try:
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        for key, value in data.items():
            setattr(enrollment, key, value)
        db.session.commit()
        logging.info(f"Matrícula actualizada: {enrollment}")
        return enrollment_schema.jsonify(enrollment)
    except Exception as e:
        logging.error(f"Error al actualizar la matrícula: {e}")
        return "Error updating enrollment", 500

def delete_enrollment(enrollment_id):
    try:
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        db.session.delete(enrollment)
        db.session.commit()
        logging.info(f"Matrícula eliminada: {enrollment}")
        return enrollment_schema.jsonify(enrollment)
    except Exception as e:
        logging.error(f"Error al eliminar la matrícula: {e}")
        return "Error deleting enrollment", 500
