# Pokermon API

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

After the disaster that happened in Oak town, Professor Oak decided that enough is enough, and he wants to share whatever data he managed to save from his labs with the public. Fortuantely, he contacted me and asked me to setup an API for people to be able to learn and study more about pokemon to prevent such disasters from ever happening again.

## API Overview

This API is pretty simple and it depends on two mainstream opensource libraries

- [Flask](https://github.com/pallets/flask)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)

And another to help with testing our code.

- [Pytest](https://github.com/pytest-dev/pytest)

### Running locally

In order to setup this locally follow these steps after cloning the project.

- setup python environment with:
  `python -m venv env && source env/bin/activate`
- install requirements with:
  `pip install -r requirements.txt`

- There are two main scripts.

1. `python run_server.py [--port <port_number>] [--debug] [--migrate]`

   This script will run the server.

   `--migrate` &nbsp; Flag to run migrations. **REQUIRED ON FIRST RUN**

   `--port` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; To run on a different port (default 5000)

   `--debug` &nbsp;&nbsp;&nbsp;&nbsp; For debuffing and hot reloading

2. `python execute.py import_pokemon --path ./Data/pokemon.csv`

   This currently only support one command **import_pokemon** to import pokemon from a csv file into the database.

### Testing

in order to execute tests, run `pytest`
