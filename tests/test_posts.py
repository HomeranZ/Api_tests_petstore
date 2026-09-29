"""
Тесты для jsonplaceholder API с разметкой Allure.
"""
import allure
import pytest
from allure_commons.types import Severity


@allure.epic("jsonplaceholder API")
@allure.feature("Posts")
class TestPosts:
    """Все тесты для ресурса /posts."""

    @allure.story("Получение постов")
    @allure.title("Получение поста по ID")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("smoke", "api")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_post_by_id(self, api_client, base_url):
        """GET /posts/1 — получаем пост по ID."""
        with allure.step(f"Отправить GET-запрос на {base_url}/posts/1"):
            response = api_client.get(f"{base_url}/posts/1")

        with allure.step("Проверить статус-код 200"):
            assert response.status_code == 200, (
                f"Ожидали 200, получили {response.status_code}"
            )

        with allure.step("Проверить поля ответа"):
            data = response.json()
            assert data["id"] == 1
            assert "title" in data

    @allure.story("Получение постов")
    @allure.title("Список всех постов")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_posts(self, api_client, base_url):
        """GET /posts — список всех постов."""
        with allure.step("Отправить GET-запрос на /posts"):
            response = api_client.get(f"{base_url}/posts")

        with allure.step("Проверить, что ответ содержит список"):
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.story("Статус-коды постов")
    @allure.title("Проверка статус-кода для разных ID")
    @allure.severity(Severity.NORMAL)
    @pytest.mark.api
    @pytest.mark.parametrize("post_id, expected_status", [
        pytest.param(1, 200, id="valid_id_1"),
        pytest.param(2, 200, id="valid_id_2"),
        pytest.param(50, 200, id="valid_id_50"),
        pytest.param(100, 200, id="valid_id_100"),
        pytest.param(999999, 404, id="nonexistent_id"),
        pytest.param(0, 404, id="invalid_id_0"),
    ])
    def test_post_statuses(self, api_client, base_url, post_id, expected_status):
        """Параметризованный тест статусов."""
        with allure.step(f"GET /posts/{post_id}"):
            response = api_client.get(f"{base_url}/posts/{post_id}")

        with allure.step(f"Проверить статус {expected_status}"):
            assert response.status_code == expected_status, (
                f"Для post_id={post_id} ожидали {expected_status}, "
                f"получили {response.status_code}"
            )

    @allure.story("Фильтрация постов")
    @allure.title("Получение постов пользователя")
    @allure.severity(Severity.MINOR)
    @pytest.mark.api
    @pytest.mark.parametrize("user_id, min_posts", [
        pytest.param(1, 1, id="user_1"),
        pytest.param(2, 1, id="user_2"),
        pytest.param(3, 1, id="user_3"),
    ])
    def test_post_by_user(self, api_client, base_url, user_id, min_posts):
        """Проверяем посты пользователя."""
        with allure.step(f"GET /posts?userId={user_id}"):
            response = api_client.get(
                f"{base_url}/posts", params={"userId": user_id}
            )

        with allure.step("Проверить структуру ответа"):
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) >= min_posts

            for post in data:
                assert "userId" in post, f"У поста {post.get('id')} нет userId"

    @allure.story("Негативные сценарии")
    @allure.title("Несуществующий ID возвращает 404")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.api
    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_id", [
        pytest.param(999999, id="id_999999"),
        pytest.param(0, id="id_0"),
        pytest.param(-1, id="id_negative"),
    ])
    def test_nonexistent_post_returns_404(self, api_client, base_url, invalid_id):
        """Негативный тест: несуществующие ID → 404."""
        with allure.step(f"GET /posts/{invalid_id}"):
            response = api_client.get(f"{base_url}/posts/{invalid_id}")

        with allure.step("Проверить статус 404"):
            assert response.status_code == 404

    @allure.story("Создание постов")
    @allure.title("Создание нового поста")
    @allure.severity(Severity.CRITICAL)
    @pytest.mark.api
    def test_create_post(self, api_client, base_url):
        """POST /posts — создаём пост."""
        new_post = {
            "title": "Pytest Post",
            "body": "This is a test",
            "userId": 1
        }

        with allure.step("Отправить POST /posts с данными"):
            response = api_client.post(f"{base_url}/posts", json=new_post)

        with allure.step("Проверить статус 201"):
            assert response.status_code == 201

        with allure.step("Проверить, что пост создан с нашими данными"):
            data = response.json()
            assert data["title"] == "Pytest Post"
            assert data["userId"] == 1
            assert "id" in data

    @allure.story("Создание постов")
    @allure.title("Использование fixture created_post")
    @allure.severity(Severity.MINOR)
    @pytest.mark.api
    def test_post_with_fixture(self, created_post):
        """Демонстрация fixture created_post."""
        with allure.step("Проверить, что fixture создала пост"):
            assert created_post["title"] == "Test Post from Fixture"
            assert created_post["userId"] == 1
            assert "id" in created_post
