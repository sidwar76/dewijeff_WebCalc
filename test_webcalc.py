import pytest
from expecter import expect

from webcalc import app
from webcalc import mongo

@pytest.fixture
def pattern():
    with app.app_context():
        mongo.db.operations.drop()
        mongo.db.operations.insert(
            dict(
                name="x",
                pattern="{{ a * b }}"
            )
        )

@pytest.fixture
def client():
    return app.test_client()

def describe_index():
    def it_says_hello(client):
        response = client.get('/')

        expect(response.data).contains(b"Hello, Someone!")

def describe_calc():
    def when_plus(client):
        response = client.get('/4/+/5')

        expect(response.data).contains(b"9")

    def from_db(client, pattern):
        response = client.get('/4/x/5')

        expect(response.data).contains(b"20")
