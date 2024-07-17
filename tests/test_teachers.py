import pytest
from app import create_app
from app.models import db, Teacher, Instrument

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/armonia_utopia'
    app.config['TESTING'] = True

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

def test_create_teacher(test_client):
    teacher = Teacher(name_teacher="Test", last_name="Teacher", telphone="1234567890", email="test@test.com")
    db.session.add(teacher)
    db.session.commit()

    retrieved_teacher = Teacher.query.filter_by(name_teacher="Test").first()
    assert retrieved_teacher is not None
    assert retrieved_teacher.last_name == "Teacher"
    assert retrieved_teacher.telphone == "1234567890"
    assert retrieved_teacher.email == "test@test.com"

    db.session.delete(retrieved_teacher)
    db.session.commit()

def test_teacher_instrument_relationship(test_client):
    teacher = Teacher(name_teacher="Music", last_name="Teacher")
    instrument = Instrument(instrument="Guitar")
    teacher.rel_instrument.append(instrument)
    db.session.add(teacher)
    db.session.add(instrument)
    db.session.commit()

    retrieved_teacher = Teacher.query.filter_by(name_teacher="Music").first()
    assert retrieved_teacher is not None
    assert len(retrieved_teacher.rel_instrument) == 1
    assert retrieved_teacher.rel_instrument[0].instrument == "Guitar"

    db.session.delete(teacher)
    db.session.delete(instrument)
    db.session.commit()