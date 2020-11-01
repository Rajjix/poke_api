from poke_api import app

def test_ping():
    response = app.test_client().get('/')
    message = response.get_json()
    assert response.status_code == 200
    assert message["data"]["msg"] == "I'm alive"


def test_pokemon():
    response = app.test_client().get('/pokemon')
    message = response.get_json()
    assert response.status_code == 200
    assert message["data"]["msg"] == "Hello, Pokemon!"