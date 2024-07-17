import pytest
from app import create_app
from app.models import db, Student

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

def test_create_student(test_client):
    student = Student(first_name="Test", last_name="Student", age=20, phone="1234567890", email="test@test.com")
    db.session.add(student)
    db.session.commit()

    retrieved_student = Student.query.filter_by(first_name="Test").first()
    assert retrieved_student is not None
    assert retrieved_student.last_name == "Student"
    assert retrieved_student.age == 20
    assert retrieved_student.phone == "1234567890"
    assert retrieved_student.email == "test@test.com"

    db.session.delete(retrieved_student)
    db.session.commit()