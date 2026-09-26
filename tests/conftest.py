import pytest
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client():
    """
    Общий HTTP-клиент для всех тестов
    scope=session - Создается один раз на всю сессию pytest
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    yield session
    session.close()


@pytest.fixture(scope="session")
def base_url():
    """базовый Url Api. Отдельный fixture легко менять"""
    return BASE_URL


@pytest.fixture
def create_post(api_client, base_url):
    """
    Создает до и удаляет после тестов.
    scope по умолчанию - function (новый для каждого теста).
    """
    new_post = {
        "title": "Test Post from Fixture",
        "body": "This is a Fixture-Generation post",
        "userId": 1
    }
    response = api_client.post(f"{base_url}/posts", json=new_post)
    assert response.status_code == 201,f"Не удалось создать пост: {response.status_code}"

    post = response.json()
    yield post
    #cleanup Удаляем пост после теста
    # (jsonplaceholder не сохраняет, а для примера, что делать)
    api_client.delete(f"{base_url}/posts/{post['id']}")

