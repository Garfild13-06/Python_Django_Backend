import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from manufacturers.models import Manufacturers
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
def create_manufacturer():
    """Фикстура для создания производителя."""
    manufacturer = Manufacturers.objects.create(
        name="Test Manufacturer",
        description="This is a test manufacturer",
        # image=None # Если нужно добавить изображение, укажите путь к файлу
    )
    return manufacturer.id  # Возвращаем id созданной чаши


@pytest.mark.django_db
def test_create_manufacturer_no_token(api_client):
    """Тест создания производителя без токена."""
    url = reverse("manufacturers-create")
    payload = {
        "name": "Test Manufacturer",
        "description": "Test Description",
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_manufacturer_token(api_client, get_token):
    """Тест создания производителя с токеном."""
    url = reverse("manufacturers-create")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {
        "name": "Test Manufacturer",
        "description": "Test Description",
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201
    assert Manufacturers.objects.filter(name="Test Manufacturer").exists()


@pytest.mark.django_db
def test_select_manufacturer_list_no_token(api_client):
    """Тест получения списка производителей без токена."""
    url = reverse("manufacturers-list")
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_select_manufacturer_list_token(api_client, get_token):
    """Тест получения списка производителей с токеном."""
    url = reverse("manufacturers-list")  # Убедитесь, что URL соответствует вашей конфигурации
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")  # Используем точечную нотацию
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve_manufacturer_no_token(api_client, create_manufacturer):
    """Тест получения конкретного производителя по UUID без токена."""
    url = reverse("manufacturers-detail", kwargs={"pk": create_manufacturer})
    print(url)
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Manufacturer"
    assert data["description"] == "This is a test manufacturer"


@pytest.mark.django_db
def test_retrieve_manufacturer_token(api_client, get_token, create_manufacturer):
    """Тест получения конкретного производителя по UUID с токеном."""
    url = reverse("manufacturers-detail", kwargs={"pk": create_manufacturer})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Manufacturer"
    assert data["description"] == "This is a test manufacturer"


@pytest.mark.django_db
def test_update_manufacturer_no_token(api_client, create_manufacturer):
    """Тест полного обновления производителя без токена."""
    url = reverse("manufacturers-update", kwargs={"pk": create_manufacturer})
    payload = {
        "name": "Updated Manufacturer",
        "description": "Updated Description",
    }
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_manufacturer_token(api_client, get_token, create_manufacturer):
    """Тест полного обновления производителя с токеном."""
    url = reverse("manufacturers-update",
                  kwargs={"pk": create_manufacturer})  # Убедитесь, что URL соответствует вашей конфигурации
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {
        "name": "Updated Manufacturer",
        "description": "Updated Description",
    }
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 200
    updated_bowl = Manufacturers.objects.get(id=create_manufacturer)
    assert updated_bowl.name == "Updated Manufacturer"


@pytest.mark.django_db
def test_partial_update_manufacturer_no_token(api_client, create_manufacturer):
    """Тест частичного обновления производителя без токена."""
    url = reverse("manufacturers-partial-update", kwargs={"pk": create_manufacturer})
    payload = {"description": "Partially Updated Description"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_manufacturer_token(api_client, get_token, create_manufacturer):
    """Тест частичного обновления производителя с токеном."""
    url = reverse("manufacturers-partial-update", kwargs={"pk": create_manufacturer})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {"description": "Partially Updated Description"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 200
    updated_bowl = Manufacturers.objects.get(id=create_manufacturer)
    assert updated_bowl.description == "Partially Updated Description"


@pytest.mark.django_db
def test_delete_manufacturer_no_token(api_client, create_manufacturer):
    """Тест удаления производителя без токена."""
    # Создаём чашу
    url = reverse("manufacturers-delete",
                  kwargs={"pk": create_manufacturer})  # Убедитесь, что URL соответствует вашей конфигурации
    response = api_client.delete(url)
    assert response.status_code == 401
    assert Manufacturers.objects.filter(id=create_manufacturer).exists()


@pytest.mark.django_db
def test_delete_manufacturer_token(api_client, get_token, create_manufacturer):
    """Тест удаления производителя с токеном."""
    # Создаём чашу
    url = reverse("manufacturers-delete",
                  kwargs={"pk": create_manufacturer})  # Убедитесь, что URL соответствует вашей конфигурации
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Manufacturers.objects.filter(id=create_manufacturer).exists()
