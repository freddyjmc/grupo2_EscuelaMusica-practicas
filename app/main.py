from sqlalchemy.orm import sessionmaker
from models import Base, engine, Student
from app.utils.app_logging import setup_logging
# Crear sesión de base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Crear un nuevo estudiant
new_student = Student(first_name='John', last_name='Doe', age=25, phone='1234567890', email='john.doe@example.com')
session.add(new_student)
session.commit()
