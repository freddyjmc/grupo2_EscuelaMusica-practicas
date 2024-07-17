import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, ForeignKey, delete
from sqlalchemy.exc import IntegrityError
from faker import Faker
from sqlalchemy import Float, ForeignKey #se agrego neuvo sugerencia claude
#from flask_login import UserMixin #añadi yo alejandra claude . INstalé flask_login
from werkzeug.security import generate_password_hash, check_password_hash #añadi yo alejandra claude, instale werkzeug
#from. import db #from app import db
import sys
sys.path.insert(0, './app')

from app import db #
from datetime import date

#db = SQLAlchemy()

# Definición de modelos

class User(db.Model): #yo alejandra añadi claude todo el codigo hasta donde dice aquí
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) #hasta aquí



class Student(db.Model):
    __tablename__ = 'students'
    id_student = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id_teacher = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_teacher = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    telphone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    rel_instrument = db.relationship('Instrument', secondary='teachers_instruments', backref='instruments_teacher')

class Instrument(db.Model):
    __tablename__ = 'instruments'
    id_instrument = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instrument = db.Column(db.String(20), nullable=False)
    pack_id = db.Column(db.Integer, db.ForeignKey('price.id_pack')) # agregado nuevo sugerencia claude
    rel_levels = db.relationship('Level', secondary="instruments_levels", backref='back_levels')

class Level(db.Model):
    __tablename__ = 'levels'
    id_level = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_level = db.Column(db.String(25))

class TeacherInstrument(db.Model):
    __tablename__ = 'teachers_instruments'
    id_teacher = db.Column('id_teacher', db.Integer, db.ForeignKey('teachers.id_teacher'), primary_key=True)
    id_instrument = db.Column('id_instrument', db.Integer, db.ForeignKey('instruments.id_instrument'), primary_key=True)

class InstrumentLevel(db.Model):
    __tablename__ = 'instruments_levels'
    id_instrument = db.Column(db.Integer, db.ForeignKey('instruments.id_instrument'), primary_key=True)
    id_level = db.Column(db.Integer, db.ForeignKey('levels.id_level'), primary_key=True)

def reset_database():
    db.session.execute(delete(InstrumentLevel))
    db.session.execute(delete(TeacherInstrument))
    db.session.execute(delete(Level))
    db.session.execute(delete(Instrument))
    db.session.execute(delete(Teacher))
    db.session.execute(delete(Student))
    db.session.commit()
    
class PriceInstrument(db.Model):
    __tablename__ = 'price'

    id_pack = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pack = db.Column(db.String(10))
    pack_price = db.Column(Float)

    #enrollments = relationship('Enrollment', secondary='price_instrument_enrollments', backref='price_instrument')
    instruments = db.relationship("Instrument", backref="pack", lazy='dynamic') # agregado nuevo sugerencia claude
    
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id_enrollment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_student = db.Column(db.Integer, ForeignKey('students.id_student'))
    id_instrument= db.Column(db.Integer, ForeignKey('instruments.id_instrument'))
    
    discount = db.Column(db.Float, default=0.0)
    enrollment_date=db.Column(db.Date) ##creé la columna para registrar la fecha
    name_student=db.Column(db.String(20))
    lastname_student=db.Column(db.String(20))
    family=db.Column(db.Boolean)    
    
    student = db.relationship("Student", backref="enrollments")
    instrument = db.relationship("Instrument", backref="enroll")
    

def populate_database():
    #reset_database() #si quito esto, me hace 'dos veces' el rellenado. Si lo dejo me salta error
    #db.create_all() #quité a la vez reset_database() y db.create_all() con el debug=True
    db.drop_all()
    db.create_all()
    

    relations = {
        "Mar": ["Piano", "Guitarra", "Batería", "Flauta"],
        "Flor": ["Piano", "Guitarra"],
        "Álvaro": ["Piano"],
        "Marifé": ["Piano", "Canto"],
        "Nayara": ["Piano", "Violín", "Bajo"],
        "Nieves":['Clarinete'],
        "Sofía": ["Percusión"]
    }

    #instruments=[]
    fake=Faker()
    for name, instrument_list in relations.items():
        teacher = Teacher(name_teacher=name, 
                          last_name=fake.last_name(),
                          telphone=fake.phone_number(),
                          email=fake.email()
                          )
        db.session.add(teacher)
        
        
        for instrument_name in instrument_list:
            instrument = Instrument.query.filter_by(instrument=instrument_name).first()
            if not instrument:
                instrument = Instrument(instrument=instrument_name)
                db.session.add(instrument)
            #instruments.append(instrument)
            teacher.rel_instrument.append(instrument)
    try:
        #db.session.flush()
        db.session.commit()
        print("Database populated successfully")
    except:
        db.session.rollback()
        print(f"Error populating database: {str(e)}")
        
            
    
    #relations
    
    relations_levels = {
        "Piano": ["Cero", "Iniciación", "Medio", "Avanzado"],
        "Guitarra": ["Iniciación", "Medio"],
        "Batería": ["Iniciación", "Medio", "Avanzado"],
        "Flauta": ["Iniciación", "Medio"],
        "Bajo": ["Iniciación", "Medio"],
        "Violin": ["Cero"],
        "Canto": ["Cero"],
        "Saxofon": ["Cero"],
        "Clarinete": ["Cero"],
        "Percusion": ["Cero"]
    }
    
    try:
        for instrument_name, levels in relations_levels.items():
            instrument = db.session.query(Instrument).filter_by(instrument=instrument_name).first()
            if not instrument:
                instrument = Instrument(instrument=instrument_name)
                db.session.add(instrument)
            
            for level_name in levels:
                level = db.session.query(Level).filter_by(name_level=level_name).first()
                if not level:
                    level = Level(name_level=level_name)
                    db.session.add(level)
                
                if level not in instrument.rel_levels:
                    instrument.rel_levels.append(level)
        
        db.session.commit()
        print("Database populated successfully")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error populating database: {str(e)}")
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {str(e)}")
    





    relations_packs = {
    "Pack_1":["Piano", "Guitarra", "Bateria", "Flauta"],
    "Pack_2":["Violin", "Bajo"],
    "Pack_3": ["Clarinete","Saxofon"],
    "Pack_4": ["Percusion", "Canto"],
    }

    list_packs={"Pack_1": 35, "Pack_2": 35, "Pack_3": 40, "Pack_4":40}
    for key, value in list_packs.items():
        price = PriceInstrument(
            pack=key,
            pack_price=value
        )
        db.session.add(price)
    
    
    """ 
    for pack, instruments in relations_packs.items():
        price = PriceInstrument(
            pack=pack,
            pack_price=list_packs[pack]
        )
        db.session.add(price)
        db.session.flush()
        for instrument_name in instruments:
            instrument = Instrument(
            instrument=instrument_name,
                pack_id=price.id_pack
            )
            db.session.add(instrument)
     """

    for pack, instruments in relations_packs.items():
        price = db.session.query(PriceInstrument).filter_by(pack=pack).first()
        for instrument_name in instruments:
            instrument = db.session.query(Instrument).filter_by(instrument=instrument_name).first()
            if not instrument:
                instrument = Instrument(instrument=instrument_name, pack=price)
                db.session.add(instrument)
            else:
                instrument.pack = price
            
    students = [
        {"first_name": "John", "last_name": "Doe", "age": 20, "phone": "123-456-7890", "email": "john.doe@example.com"},
        {"first_name": "Jane", "last_name": "Smith", "age": 22, "phone": "098-765-4321", "email": "jane.smith@example.com"},
        {"first_name": "Michael", "last_name": "Johnson", "age": 25, "phone": "555-123-4567", "email": "michael.johnson@example.com"},
        {"first_name": "Emily", "last_name": "Williams", "age": 21, "phone": "789-012-3456", "email": "emily.williams@example.com"},
    ]

    for student in students:
        new_student = Student(**student)
        db.session.add(new_student)
    db.session.commit()

    result = db.session.query(Student).all()
    
    """ 
    list=["Piano", "Guitarra", "Bateria","Violin","Canto", "Flauta","Saxofon","Clarinete", "Percusión", "Bajo"]
    for i in range(len(list)):
        instruments=Instrument(
            instrument=list[i]
        )
        db.session.add(instruments)

     """
    
    try:
        students = db.session.query(Student).all()
        instruments = db.session.query(Instrument).all()

        if not students or not instruments:
            print("No hay estudiantes o instrumentos en la base de datos.")
        else:
            for student in students:
                instrument = random.choice(instruments)
                enrollment = Enrollment(
                    id_student=student.id_student,
                    id_instrument=instrument.id_instrument,
                    enrollment_date=fake.date(),   #---------
                    name_student=student.email,
                    lastname_student=student.last_name,
                    family=fake.boolean()
                )
                db.session.add(enrollment)

        db.session.commit()
        print("Inscripciones creadas con éxito.")
    except Exception as e:
        print(f"Error al crear inscripciones: {e}")
        db.session.rollback()

    db.session.commit()

#Creo que la función enrollment hay que sacarla de la función que puebla las tablas
def enroll_student(instrument_id, name, lastname, fam, enroll_date=date.today()):
    existing_student = db.session.query(Student).filter_by(first_name=name, last_name=lastname).first()
    new_instrument = db.session.query(Instrument).get(instrument_id)
    
    #Primero veo si el estudiante existe, y si existe me guardo su id
    if existing_student:
        student_id = existing_student.id_student

    else:
    # Verificar si el estudiante ya está inscrito en otro instrumento del mismo pack
        new_student = db.Student(first_name=name, last_name=lastname) 
        db.session.add(new_student) 
        db.sesion.flush() # Esto asigna un id al nuevo estudiante, porque recuerda el autoincrement
        student_id = new_student.id_student
        
        # Crear una nueva inscripción sin descuento para el nuevo estudiante
        new_enrollment = Enrollment(
            id_student=student_id, 
            id_instrument=instrument_id,
            name_student=name,
            lastname_student=lastname,
            enrollment_date=enroll_date,
            discount=0.0,
            family=fam,
            
        )
        db.session.add(new_enrollment)
        db.session.commit()
        f"Nueva inscripción creada sin descuento"
        return new_enrollment # "Nueva inscripción creada sin descuento"        
        
    # Verificamos si el estudiante ya está inscrito en otros instrumentos del mismo pack
    existing_enrollments = db.session.query(Enrollment).filter_by(id_student=student_id).all()
    same_pack_enrollments = [
        enrollment for enrollment in existing_enrollments 
        if enrollment.instrument.pack_id == new_instrument.pack_id
    ]
    
    if len(same_pack_enrollments) >= 2:
        # Si ya está inscrito en 2 o más instrumentos del mismo pack, aplicar 75% de descuento
        discount = 0.75
    elif len(same_pack_enrollments) == 1:
        # Si está inscrito en 1 instrumento del mismo pack, aplicar 50% de descuento
        discount = 0.5
    else:
        # Si no está inscrito en ningún instrumento del mismo pack, no hay descuento
        discount = 0.0        
        
    # Crear nueva inscripción con el descuento correspondiente y.....
    new_enrollment = Enrollment(
        id_student=student_id, 
        id_instrument=instrument_id, 
        discount=discount, 
        enrollment_date=enroll_date,
        name_student=name,
        lastname_student=lastname,
        family=fam
    )
    db.session.add(new_enrollment)     
    
    
    
    # Aplica el mismo descuento a las inscripciones ya existentes del mismo pack
    for enrollment in same_pack_enrollments:
        enrollment.discount = discount
    
    db.session.commit()
    f"Inscripción creada con {discount*100}% de descuento"
    return new_enrollment #f"Inscripción creada con {discount*100}% de descuento"
    

def get_final_price(enrollment_id):
    enrollment = db.session.query(Enrollment).get(enrollment_id)
    pack_price = enrollment.instrument.pack.pack_price
    discount = enrollment.discount
    
    price_discount=pack_price*(1-discount)
    if enrollment.family==True:
        family_discount=0.10
        price_discount=price_discount*(1-family_discount)
        return price_discount
    else:
        return price_discount
    
"""     
# Creo un nueva inscripción (que puede ser tanto de un estudiante nuevo, como de uno ya registrado) #LaQuito de aquí y la pongo en run.py
#result = enroll_student(instrument_id=1, name='John',lastname='Doe', fam=True, enroll_date=date.today())
#print(result)
#db.session.commit() #Hay que hacer commit


# Obtener el precio final de una inscripción, cada una
final_price = get_final_price(enrollment_id=1)
print(f"Precio final: {final_price}")


# Verificar las inscripciones
enrollments = db.session.query(Enrollment).filter_by(id_student=1).all()
if enrollments:
    for enrollment in enrollments:
        print(f"Inscripción: {enrollment.id_enrollment}, Estudiante: {enrollment.id_student}, Instrumento: {enrollment.id_instrument}")
else:
    print("No se encontraron inscripciones para el estudiante 1")

db.session.commit()

try:
    db.session.commit()
    print("Base de datos poblada exitosamente.")
except IntegrityError as e:
    db.session.rollback()
    print(f"Error de integridad: {str(e)}")
except Exception as e:
    db.session.rollback()
    print(f"Error inesperado: {str(e)}")

 """

def init_db(app):
    with app.app_context():
        db.drop_all()  # Esto eliminará todas las tablas existente #se agrego nuevo sugerencia claude
        #db.create_all()
        
        #populate_database() lo he eliminado porque la llamo en run.py
