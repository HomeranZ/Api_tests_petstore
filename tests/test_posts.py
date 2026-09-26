"""
Тесты для jsonplaceholder API.
Используют fixtures из conftest.py: api_client, base_url, created_post.
"""
from http.client import responses

import pytest


# Базовые тесты проверяющие жив ли API

@pytest.mark.smoke
@pytest.mark.api
def test_get_post_by_id(api_client, base_url):
    """GET /posts/1 — получаем пост по ID."""
    response = api_client.get(f"{base_url}/posts/1")
    
    assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
    data = response.json()
    assert "id" in data
    assert data["id"] == 1


@pytest.mark.smoke
@pytest.mark.api
def test_get_all_posts(api_client, base_url):
    """GET /posts — список всех постов."""
    response = api_client.get(f"{base_url}/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.api
@pytest.mark.parametrize("post_id, expected_status", [
    (1, 200),    # валидный id
    (2, 200),
    (50, 200),
    (100, 200),
    (999999, 404),   # Несуществующий id
    (0, 404)     # НЕ валидный id
])
def test_post_statuses(api_client, base_url, post_id, expected_status):
    """Параметрезированный тест"""
    response = api_client.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == expected_status, (
        f"Для post_id{post_id} ожидали {expected_status},"
        f"Получили {response.status_code}"
    )


@pytest.mark.api
@pytest.mark.parametrize("user_id, min_posts", [
    (1, 1),
    (2, 1),
    (3, 1),
])
def test_post_by_user(api_client, base_url, user_id, min_posts):
    """
    Параметризация с фильтром: проверяем, что у каждого пользователя >= N постов.
    """
    response = api_client.get(f"{base_url}/posts", params={"userId": user_id})
    assert response.status_code == 200
    data = response.json()
    # jsonplaceholder возвращает ВСЕ посты независимо от фильтра,
    # поэтому проверяем, что ответ не пустой
    assert isinstance(data, list)
    assert len(data) >= min_posts
    for post in data:
        assert "userId" in post, f'У поста {post.get("id")} нет поля userId'

# Проверка на поведение при ошибках

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", [
    999999,
    0,
    -1,
])
def test_nonexistent_post_returns_404(api_client,base_url,invalid_id):
    """Негативный тест на несуществующие id -> 404"""
    response = api_client.get(f'{base_url}/posts/{invalid_id}')
    assert response.status_code == 404

# Тесты с созданием данных

@pytest.mark.api
def test_create_post(api_client, base_url):
    """POST /posts — создаём пост."""
    new_post = {
        "title": "Pytest Post",
        "body": "This is a test",
        "userId": 1
    }
    response = api_client.post(f"{base_url}/posts", json=new_post)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Pytest Post"
    assert data["userId"] == 1
    # jsonplaceholder присваивает id = 101 новым постам
    assert "id" in data

@pytest.mark.api
def test_post_with_fixture(create_post):
    """
    Используем fixture 'create_post'
    Пост создается до теста и удаляется после что и делает conftest.
    """

    # create_posn - готовый json-объект из fixture
    assert create_post["title"] == "Test Post from Fixture"
    assert create_post["userId"] == 1
    assert "id" in create_post
