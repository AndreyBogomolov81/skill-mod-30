def test_get_home(client):
    res = client.get('/home')
    assert 200 == res.status_code

def test_add_recipe(client):
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

def test_recipe_get_by_id(client):
    resp = client.get('/recipes/1')
    assert resp.status_code == 200

def test_recipes_get_all(client):
    resp = client.get('/recipes/')
    assert resp.status_code == 200