import pytest
from app import create_app
from app.models import db, Instrument, Level

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

def test_create_instrument(test_client):
    instrument = Instrument(instrument="Piano")
    db.session.add(instrument)
    db.session.commit()

    retrieved_instrument = Instrument.query.filter_by(instrument="Piano").first()
    assert retrieved_instrument is not None
    assert retrieved_instrument.instrument == "Piano"

    db.session.delete(retrieved_instrument)
    db.session.commit()

def test_instrument_level_relationship(test_client):
    instrument = Instrument(instrument="Violin")
    level = Level(name_level="Beginner")
    instrument.rel_levels.append(level)
    db.session.add(instrument)
    db.session.add(level)
    db.session.commit()

    retrieved_instrument = Instrument.query.filter_by(instrument="Violin").first()
    assert retrieved_instrument is not None
    assert len(retrieved_instrument.rel_levels) == 1
    assert retrieved_instrument.rel_levels[0].name_level == "Beginner"

    db.session.delete(instrument)
    db.session.delete(level)
    db.session.commit()