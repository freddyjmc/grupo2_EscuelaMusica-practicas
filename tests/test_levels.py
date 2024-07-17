import pytest
from app import create_app
from app.models import db, Level, Instrument

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

def test_create_level(test_client):
    level = Level(name_level="Intermediate")
    db.session.add(level)
    db.session.commit()

    retrieved_level = Level.query.filter_by(name_level="Intermediate").first()
    assert retrieved_level is not None
    assert retrieved_level.name_level == "Intermediate"

    db.session.delete(retrieved_level)
    db.session.commit()

def test_level_instrument_relationship(test_client):
    level = Level(name_level="Advanced")
    instrument = Instrument(instrument="Saxophone")
    level.back_levels.append(instrument)
    db.session.add(level)
    db.session.add(instrument)
    db.session.commit()

    retrieved_level = Level.query.filter_by(name_level="Advanced").first()
    assert retrieved_level is not None
    assert len(retrieved_level.back_levels) == 1
    assert retrieved_level.back_levels[0].instrument == "Saxophone"

    db.session.delete(level)
    db.session.delete(instrument)
    db.session.commit()