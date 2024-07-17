import pytest
from app import create_app, db
from app.models import Enrollment, Student, Level, Instrument, Teacher

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    return app

@pytest.fixture(scope='module')
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_create_enrollment(init_database):
    with init_database.app.app_context():
        # Crear un estudiante, nivel, instrumento y profesor
        student = Student(first_name='John', last_name='Doe', age=25, phone='1234567890', email='john.doe@example.com')
        level = Level(name_level='Iniciación')
        instrument = Instrument(instrument='Piano')
        teacher = Teacher(name_teacher='Maria Gomez')
        db.session.add_all([student, level, instrument, teacher])
        db.session.commit()

        # Crear una nueva inscripción
        enrollment = Enrollment(
            id_student=student.id_student,
            id_level=level.id_level,
            id_instrument=instrument.id_instrument,
            id_teacher=teacher.id_teacher,
            base_price=35.0,
            final_price=35.0,
            family_discount=False
        )
        db.session.add(enrollment)
        db.session.commit()

        # Verificar que la inscripción se creó correctamente
        assert enrollment.id_student == student.id_student
        assert enrollment.id_level == level.id_level
        assert enrollment.id_instrument == instrument.id_instrument
        assert enrollment.id_teacher == teacher.id_teacher
        assert enrollment.base_price == 35.0
        assert enrollment.final_price == 35.0
        assert not enrollment.family_discount

def test_update_enrollment(init_database):
    with init_database.app.app_context():
        # Crear una nueva inscripción
        student = Student(first_name='Jane', last_name='Smith', age=30, phone='9876543210', email='jane.smith@example.com')
        level = Level(name_level='Avanzado')
        instrument = Instrument(instrument='Guitarra')
        teacher = Teacher(name_teacher='Carlos Rodriguez')
        db.session.add_all([student, level, instrument, teacher])
        db.session.commit()

        enrollment = Enrollment(
            id_student=student.id_student,
            id_level=level.id_level,
            id_instrument=instrument.id_instrument,
            id_teacher=teacher.id_teacher,
            base_price=40.0,
            final_price=40.0,
            family_discount=False
        )
        db.session.add(enrollment)
        db.session.commit()

        # Actualizar la inscripción
        enrollment.final_price = 35.0
        enrollment.family_discount = True
        db.session.commit()

        # Verificar que la inscripción se actualizó correctamente
        updated_enrollment = Enrollment.query.get(enrollment.id_enrollment)
        assert updated_enrollment.final_price == 35.0
        assert updated_enrollment.family_discount

def test_delete_enrollment(init_database):
    with init_database.app.app_context():
        # Crear una nueva inscripción
        student = Student(first_name='Alice', last_name='Johnson', age=22, phone='5555555555', email='alice.johnson@example.com')
        level = Level(name_level='Intermedio')
        instrument = Instrument(instrument='Violín')
        teacher = Teacher(name_teacher='Laura Martinez')
        db.session.add_all([student, level, instrument, teacher])
        db.session.commit()

        enrollment = Enrollment(
            id_student=student.id_student,
            id_level=level.id_level,
            id_instrument=instrument.id_instrument,
            id_teacher=teacher.id_teacher,
            base_price=45.0,
            final_price=45.0,
            family_discount=False
        )
        db.session.add(enrollment)
        db.session.commit()

        # Eliminar la inscripción
        db.session.delete(enrollment)
        db.session.commit()

        # Verificar que la inscripción se eliminó correctamente
        deleted_enrollment = Enrollment.query.get(enrollment.id_enrollment)