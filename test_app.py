import os
import pytest
import sys
sys.path.insert(1, '../')
import app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert b'Number of Containers' in rv.data