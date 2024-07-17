from flask import Blueprint, render_template


frontend_bp = Blueprint('frontend', __name__)

# Ruta para la página principal

@frontend_bp.route('/')
def index():
    return render_template('index.html')


@frontend_bp.route('/enrollments')
def enrollments():
    return render_template('enrollments.html')

@frontend_bp.route('/instruments')
def instruments():
    return render_template('instruments.html')

@frontend_bp.route('/levels')
def levels():
    return render_template('levels.html')

@frontend_bp.route('/students')
def students():
    return render_template('students.html')

@frontend_bp.route('/teachers')
def teachers():
    return render_template('teachers.html')