import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


# DATABASES
DATABASE_NAME = 'pokemon.sqlite'
DATABASE_URL = f"sqlite:///{BASE_DIR}/{DATABASE_NAME}"
