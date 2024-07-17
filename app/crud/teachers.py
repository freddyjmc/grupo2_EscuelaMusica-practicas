import logging
from app.models import Teacher
from app.schemas import teacher_schema, teachers_schema
from app import db

# Configura el nivel de registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_teacher(data):
    new_teacher = Teacher(**data)
    db.session.add(new_teacher)
    db.session.commit()
    return teacher_schema.jsonify(new_teacher)
    try:
        new_teacher = Teacher(**data)
        db.session.add(new_teacher)
        db.session.commit()
        logging.info(f"Profesor agregado: {new_teacher}")
        return teacher_schema.jsonify(new_teacher)
    except Exception as e:
        logging.error(f"Error al agregar profesor: {e}")
        return "Error adding teacher", 500

def get_all_teachers():
    teachers = Teacher.query.all()
    return teachers_schema.dump(teachers)
    try:
        teachers = Teacher.query.all()
        logging.info(f"Se obtuvieron {len(teachers)} profesores")
        return teachers_schema.dump(teachers)
    except Exception as e:
        logging.error(f"Error al obtener profesores: {e}")
        return "Error fetching teachers", 500

def get_teacher_by_id(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return teacher_schema.jsonify(teacher)
    try:
        teacher = Teacher.query.get_or_404(teacher_id)
        logging.info(f"Se obtuvo el profesor: {teacher}")
        return teacher_schema.jsonify(teacher)
    except Exception as e:
        logging.error(f"Error al obtener el profesor por ID: {e}")
        return "Error fetching teacher", 404

def update_teacher(teacher_id, data):
    teacher = Teacher.query.get_or_404(teacher_id)
    for key, value in data.items():
        setattr(teacher, key, value)
    db.session.commit()
    return teacher_schema.jsonify(teacher)
    try:
        teacher = Teacher.query.get_or_404(teacher_id)
        for key, value in data.items():
            setattr(teacher, key, value)
        db.session.commit()
        logging.info(f"Profesor actualizado: {teacher}")
        return teacher_schema.jsonify(teacher)
    except Exception as e:
        logging.error(f"Error al actualizar el profesor: {e}")
        return "Error updating teacher", 500

def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return teacher_schema.jsonify(teacher)
    try:
        teacher = Teacher.query.get_or_404(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        logging.info(f"Profesor eliminado: {teacher}")
        return teacher_schema.jsonify(teacher)
    except Exception as e:
        logging.error(f"Error al eliminar el profesor: {e}")
        return "Error deleting teacher", 500