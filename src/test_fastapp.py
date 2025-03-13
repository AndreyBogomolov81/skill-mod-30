from fastapi.testclient import TestClient

from fastapp import app

client = TestClient(app)

def test_get_home():
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