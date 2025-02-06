import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from main.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    """Создание тестового пользователя."""
    user = CustomUser.objects.create_user(
        email="testuser@example.com",
        username="testuser",
        password="password123",
    )
    return user


@pytest.fixture
def get_token(api_client, create_user):
    """Получение JWT-токена для зарегистрированного пользователя."""
    url = reverse("jwt-create")  # Убедитесь, что URL соответствует вашей конфигурации
    payload = {
        "email": create_user.email,  # Используем точечную нотацию
        "password": "password123",  # Пароль передается явно
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200
    responce_data = {
        "access": response.json()["data"]["access"],  # Токены находятся в корне JSON
        "refresh": response.json()["data"]["refresh"]
    }
    return responce_data


@pytest.mark.django_db
def test_get_token_for_existing_user(api_client, create_user):
    """
    Тест: Получение JWT-токена для существующего пользователя.
    """
    # URL для получения токена
    url = reverse("jwt-create")  # Убедитесь, что имя маршрута совпадает
    # Данные для запроса
    payload = {
        "email": create_user.email,  # Используем точечную нотацию
        "password": "password123",  # Пароль передается явно
    }
    # Выполняем POST-запрос
    response = api_client.post(url, data=payload, format="json")
    # Проверяем статус код
    assert response.status_code == 200
    # Проверяем структуру ответа
    data = response.json()["data"]  # Токены находятся в корне JSON
    assert "access" in data
    assert "refresh" in data
    assert isinstance(data["access"], str)
    assert isinstance(data["refresh"], str)
    # Выводим токены для отладки
    print("Access Token:", data["access"])
    print("Refresh Token:", data["refresh"])


@pytest.mark.django_db
def test_get_token_for_not_existing_user(api_client):
    """
    Тест: Попытка получения JWT-токена для НЕсуществующего пользователя.
    """
    # URL для получения токена
    url = reverse("jwt-create")  # Убедитесь, что имя маршрута совпадает
    # Данные для запроса
    payload = {
        "email": "unreal@user.dot",
        "password": "3w487h65v2",
    }
    # Выполняем POST-запрос
    response = api_client.post(url, data=payload, format="json")
    print(response.json())
    # Проверяем статус код
    assert response.status_code == 401
