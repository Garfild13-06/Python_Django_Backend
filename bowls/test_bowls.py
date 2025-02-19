import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from bowls.models import Bowls
from users.models import CustomUser


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


@pytest.fixture
def create_bowl():
    """Фикстура для создания чаши."""
    bowl = Bowls.objects.create(
        type="Test Bowl",
        description="This is a test bowl",
        howTo="Instructions for using the bowl",
        # image=None  # Если нужно добавить изображение, укажите путь к файлу
    )
    return bowl.id  # Возвращаем id созданной чаши


@pytest.mark.django_db
def test_create_bowl_no_token(api_client):
    """Тест создания чаши без токена."""
    url = reverse("bowls-create")
    payload = {
        "type": "Test Bowl",
        "description": "Test Description",
        "howTo": "Test Instructions",
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_bowl_token(api_client, get_token):
    """Тест создания чаши с токеном."""
    url = reverse("bowls-create")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {
        "type": "Test Bowl",
        "description": "Test Description",
        "howTo": "Test Instructions",
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201
    assert Bowls.objects.filter(type="Test Bowl").exists()


@pytest.mark.django_db
def test_select_bowls_list_no_token(api_client):
    """Тест получения списка чаш без токена."""
    url = reverse("bowls-list")
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_select_bowls_list_token(api_client, get_token):
    """Тест получения списка чаш с токеном."""
    url = reverse("bowls-list")  # Убедитесь, что URL соответствует вашей конфигурации
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")  # Используем точечную нотацию
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve_bowl_no_token(api_client, create_bowl):
    """Тест получения конкретной чаши по UUID без токена."""
    url = reverse("bowls-detail", kwargs={"pk": create_bowl})
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["type"] == "Test Bowl"
    assert data["description"] == "This is a test bowl"
    assert data["howTo"] == "Instructions for using the bowl"


@pytest.mark.django_db
def test_retrieve_bowl_token(api_client, get_token, create_bowl):
    """Тест получения конкретной чаши по UUID с токеном."""
    url = reverse("bowls-detail", kwargs={"pk": create_bowl})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["type"] == "Test Bowl"
    assert data["description"] == "This is a test bowl"
    assert data["howTo"] == "Instructions for using the bowl"


@pytest.mark.django_db
def test_update_bowl_no_token(api_client, create_bowl):
    """Тест полного обновления чаши без токена."""
    url = reverse("bowls-update", kwargs={"pk": create_bowl})
    payload = {
        "type": "Updated Bowl",
        "description": "Updated Description",
        "howTo": "Updated Instructions",
    }
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_bowl_token(api_client, get_token, create_bowl):
    """Тест полного обновления чаши с токеном."""
    url = reverse("bowls-update", kwargs={"pk": create_bowl})  # Убедитесь, что URL соответствует вашей конфигурации
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {
        "type": "Updated Bowl",
        "description": "Updated Description",
        "howTo": "Updated Instructions",
    }
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 200
    updated_bowl = Bowls.objects.get(id=create_bowl)
    assert updated_bowl.type == "Updated Bowl"


@pytest.mark.django_db
def test_partial_update_bowl_no_token(api_client, create_bowl):
    """Тест частичного обновления чаши без токена."""
    url = reverse("bowls-partial-update", kwargs={"pk": create_bowl})
    payload = {"description": "Partially Updated Description"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_bowl_token(api_client, get_token, create_bowl):
    """Тест частичного обновления чаши с токеном."""
    url = reverse("bowls-partial-update", kwargs={"pk": create_bowl})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {"description": "Partially Updated Description"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 200
    updated_bowl = Bowls.objects.get(id=create_bowl)
    assert updated_bowl.description == "Partially Updated Description"


@pytest.mark.django_db
def test_delete_bowl_no_token(api_client, create_bowl):
    """Тест удаления чаши без токена."""
    # Создаём чашу
    url = reverse("bowls-delete",
                  kwargs={"pk": create_bowl})  # Убедитесь, что URL соответствует вашей конфигурации
    response = api_client.delete(url)
    assert response.status_code == 401
    assert Bowls.objects.filter(id=create_bowl).exists()


@pytest.mark.django_db
def test_delete_bowl_token(api_client, get_token, create_bowl):
    """Тест удаления чаши с токеном."""
    # Создаём чашу
    url = reverse("bowls-delete",
                  kwargs={"pk": create_bowl})  # Убедитесь, что URL соответствует вашей конфигурации
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Bowls.objects.filter(id=create_bowl).exists()
