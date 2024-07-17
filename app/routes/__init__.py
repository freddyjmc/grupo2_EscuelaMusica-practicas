from flask import Blueprint
from app.routes.students import students_bp
from app.routes.teachers import teachers_bp
from app.routes.levels import levels_bp
from app.routes.instruments import instruments_bp
from app.routes.enrollments import enrollments_bp
from app.routes.auth import auth_bp #lo agregué alejandra claude

# Blueprint registration
__all__ = [
    'students_bp',
    'teachers_bp',
    'levels_bp',
    'instruments_bp',
    'enrollments_bp',
    'auth_bp' #lo agregué alejandra claude

]
