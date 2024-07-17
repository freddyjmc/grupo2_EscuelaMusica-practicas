from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import pymysql
pymysql.install_as_MySQLdb()
import os
import sys #puse esto
from app.utils.app_logging import setup_logger #añadi esto alejandra


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #puse esto



# Cargar variables de entorno
load_dotenv()

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    if config_name == 'production':
        app.config.from_object('app.config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Configuración del logger
    setup_logger(app)  #lo añadi alejandra claude

    # Registrar rutas
    from app.routes.students import students_bp
    from app.routes.teachers import teachers_bp
    from app.routes.levels import levels_bp
    from app.routes.instruments import instruments_bp
    from app.routes.enrollments import enrollments_bp
    from app.routes.auth import auth_bp #lo añadi alejandra claude

    app.register_blueprint(students_bp)
    app.register_blueprint(teachers_bp)
    app.register_blueprint(levels_bp)
    app.register_blueprint(instruments_bp)
    app.register_blueprint(enrollments_bp)
    app.register_blueprint(auth_bp) #lo añadi alejandra claude

    with app.app_context():
        db.create_all()
        

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run()
