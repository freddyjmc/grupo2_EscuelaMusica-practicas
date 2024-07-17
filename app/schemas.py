from app import ma
from app.models import Student, Teacher, Level, Instrument, Enrollment, PriceInstrument, InstrumentLevel, TeacherInstrument
from marshmallow import fields

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        include_fk = True
        load_instance = True
    id_student = ma.auto_field(dump_only=True)
    enrollments = fields.Nested('EnrollmentSchema', many=True, exclude=('student',))

class TeacherSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        include_fk = True
        load_instance = True
    id_teacher = ma.auto_field(dump_only=True)
    instruments = fields.Nested('TeacherInstrumentSchema', many=True, exclude=('teacher',))

    class TeacherInstrumentSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = TeacherInstrument
            include_fk = True
            load_instance = True
class LevelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Level
        include_fk = True
        load_instance = True
    id_level = ma.auto_field(dump_only=True)
    instruments = fields.Nested('InstrumentLevelSchema', many=True, exclude=('level',))

class InstrumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Instrument
        include_fk = True
        load_instance = True
    id_instrument = ma.auto_field(dump_only=True)
    teacher_instruments = fields.Nested('TeacherInstrumentSchema', many=True, exclude=('instrument',))
    instrument_levels = fields.Nested('InstrumentLevelSchema', many=True, exclude=('instrument',))
    enrollments = fields.Nested('EnrollmentSchema', many=True, exclude=('instrument',))

class EnrollmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Enrollment
        include_fk = True
        load_instance = True
    id_enrollment = ma.auto_field(dump_only=True)
    student = fields.Nested(StudentSchema, exclude=('enrollments',))
    instrument = fields.Nested(InstrumentSchema, exclude=('enrollments',))
    teacher = fields.Nested(TeacherSchema, exclude=('instruments',))
    level = fields.Nested(LevelSchema, exclude=('instruments',))

class PriceInstrumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PriceInstrument
        include_fk = True
        load_instance = True
    id_pack = ma.auto_field(dump_only=True)
class InstrumentLevelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InstrumentLevel
        include_fk = True
        load_instance = True

# Inicializamos los schemas
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)
level_schema = LevelSchema()
levels_schema = LevelSchema(many=True)
instrument_schema = InstrumentSchema()
instruments_schema = InstrumentSchema(many=True)
enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)
price_instrument_schema = PriceInstrumentSchema()
price_instruments_schema = PriceInstrumentSchema(many=True)
instrument_level_schema = InstrumentLevelSchema()
instruments_levels_schema = InstrumentLevelSchema(many=True)