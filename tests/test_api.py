import time
from fastapi.testclient import TestClient
import pytest

from nikita.src.main import app

test_client = TestClient(app)


def test_root():
    response = test_client.post("/")
    assert response.status_code == 200
    assert response.json() == {"ok":200}


def test_get_recipes():
    response = test_client.get("/recipes")
    assert response.status_code == 200
    resp = response.json()

def test_get_recipes_by_id(recipes_id=1):
    response = test_client.get(f"/recipes/{recipes_id}")
    assert response.status_code == 200
    resp = response.json()


def test_create_recipes():
    response = test_client.post("/recipes")
    assert response.status_code == 422
    # assert response.json() == {"ok":True}


