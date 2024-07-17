from flask import Flask
from app import create_app
from app.models import populate_database,enroll_student, get_final_price
from datetime import date
from app import db
from app.models import Enrollment, Student, Instrument

if __name__ == "__main__":
    app = create_app() #primero hay que instanciar la importación que hacemos de from app import create_app
    with app.app_context(): #Hay que ejecutar la función que inserta los datos dentro del contexto de la aplicación para que esa función tenga acceso a la sesión de la base de datos correcta.
        populate_database()
        result = enroll_student(instrument_id=1, name='John', lastname='Doe', fam=True, enroll_date=date.today())
        final_price = get_final_price(enrollment_id=1)
        db.session.commit()
    
    app.run(debug=True)  # IMPORTANTE: Lo quito si no es necesario ejecutar el servidor de desarrollo, así impide que se llame varias veces y acumule datos

# Obtener el precio final de una inscripción, cada una
print(f"Precio final: {final_price}")

"""     app = create_app()
    #populate_database()
    app.run(debug=True)
 """
#hay que llamar a la función que inserta los datos en las tablas, pero DEPUÉS de inicializar
#la aplicación y la base de datos
