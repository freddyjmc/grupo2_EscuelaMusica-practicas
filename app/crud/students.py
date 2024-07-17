import logging
from app.models import Student
from app.schemas import student_schema, students_schema
from app import db

# Configura el nivel de registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_student(data):
    try:
        new_student = Student(**data)
        db.session.add(new_student)
        db.session.commit()
        logging.info(f"Estudiante agregado: {new_student}")
        return student_schema.jsonify(new_student)
    except Exception as e:
        logging.error(f"Error al agregar estudiante: {e}")
        return "Error adding student", 500

def get_all_students():
    try:
        students = Student.query.all()
        logging.info(f"Se obtuvieron {len(students)} estudiantes")
        return students_schema.dump(students)
    except Exception as e:
        logging.error(f"Error al obtener estudiantes: {e}")
        return "Error fetching students", 500

def get_student_by_id(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        logging.info(f"Se obtuvo el estudiante: {student}")
        return student_schema.jsonify(student)
    except Exception as e:
        logging.error(f"Error al obtener el estudiante por ID: {e}")
        return "Error fetching student", 404

def update_student(student_id, data):
    try:
        student = Student.query.get_or_404(student_id)
        for key, value in data.items():
            setattr(student, key, value)
        db.session.commit()
        logging.info(f"Estudiante actualizado: {student}")
        return student_schema.jsonify(student)
    except Exception as e:
        logging.error(f"Error al actualizar el estudiante: {e}")
        return "Error updating student", 500

def delete_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        logging.info(f"Estudiante eliminado: {student}")
        return student_schema.jsonify(student)
    except Exception as e:
        logging.error(f"Error al eliminar el estudiante: {e}")
        return "Error deleting student", 500