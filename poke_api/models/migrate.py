from .pokemon import Pokemon
from . import db


def run_migrations(app):
    """
    setup database tables.
    IMPORTANT: make sure you have import all required models.
    """
    with app.app_context():
        db.create_all()
        db.session.commit()
