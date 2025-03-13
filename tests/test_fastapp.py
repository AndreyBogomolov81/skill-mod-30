# from fastapi.testclient import TestClient
# import pytest
#
# from src.fastapp import app
#
#
# client = TestClient(app)

import pytest
from httpx import AsyncClient


def test_get_home(client: AsyncClient):
    res = client.get('/home')
    assert 200 == res.status_code

def test_add_recipe():
    response = client.post(
        "/recipes/",
        json={
            "title": "рецепт 5",
            "cooking_time": 50,
            "ingredients": "ингридиет 1",
            "description": "отличное блюдо"
        },
    )

    assert response.status_code == 201

def test_recipe_get_by_id(client: AsyncClient):
    resp = client.get('/recipes/1')
    assert resp.status_code == 200

def test_recipes_get_all(client: AsyncClient):
    resp = client.get('/recipes/')
    assert resp.status_code == 200