import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tastecategories.models import TasteCategories
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
def create_tastecategory():
    """Фикстура для создания категории вкусов."""
    category = TasteCategories.objects.create(name="Test Category")
    return category.id


# Тесты для создания категории вкусов
@pytest.mark.django_db
def test_create_tastecategory_no_token(api_client):
    """Тест создания категории вкусов без токена."""
    url = reverse("tastecategories-create")
    payload = {"name": "Test Category"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_tastecategory_with_token(api_client, get_token):
    """Тест создания категории вкусов с токеном."""
    url = reverse("tastecategories-create")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {"name": "Test Category"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201
    assert TasteCategories.objects.filter(name="Test Category").exists()


# Тесты для получения списка категорий вкусов
@pytest.mark.django_db
def test_list_tastecategories_no_token(api_client):
    """Тест получения списка категорий вкусов без токена."""
    url = reverse("tastecategories-list")
    response = api_client.post(url, format="json")
    print(response)
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_tastecategories_with_token(api_client, get_token):
    """Тест получения списка категорий вкусов с токеном."""
    url = reverse("tastecategories-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200


# Тесты для получения деталей категории вкусов
@pytest.mark.django_db
def test_retrieve_tastecategory_no_token(api_client, create_tastecategory):
    """Тест получения деталей категории вкусов без токена."""
    url = reverse("tastecategories-detail", kwargs={"pk": create_tastecategory})
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Category"


@pytest.mark.django_db
def test_retrieve_tastecategory_with_token(api_client, get_token, create_tastecategory):
    """Тест получения деталей категории вкусов с токеном."""
    url = reverse("tastecategories-detail", kwargs={"pk": create_tastecategory})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Category"


# Тесты для обновления категории вкусов
@pytest.mark.django_db
def test_update_tastecategory_no_token(api_client, create_tastecategory):
    """Тест полного обновления категории вкусов без токена."""
    url = reverse("tastecategories-update", kwargs={"pk": create_tastecategory})
    payload = {"name": "Updated Category"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_tastecategory_with_token(api_client, get_token, create_tastecategory):
    """Тест полного обновления категории вкусов с токеном."""
    url = reverse("tastecategories-update", kwargs={"pk": create_tastecategory})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {"name": "Updated Category"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 200
    updated_category = TasteCategories.objects.get(id=create_tastecategory)
    assert updated_category.name == "Updated Category"


# Тесты для частичного обновления категории вкусов
@pytest.mark.django_db
def test_partial_update_tastecategory_no_token(api_client, create_tastecategory):
    """Тест частичного обновления категории вкусов без токена."""
    url = reverse("tastecategories-partial-update", kwargs={"pk": create_tastecategory})
    payload = {"name": "Partially Updated Category"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_tastecategory_with_token(api_client, get_token, create_tastecategory):
    """Тест частичного обновления категории вкусов с токеном."""
    url = reverse("tastecategories-partial-update", kwargs={"pk": create_tastecategory})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {"name": "Partially Updated Category"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 200
    updated_category = TasteCategories.objects.get(id=create_tastecategory)
    assert updated_category.name == "Partially Updated Category"


# Тесты для удаления категории вкусов
@pytest.mark.django_db
def test_delete_tastecategory_no_token(api_client, create_tastecategory):
    """Тест удаления категории вкусов без токена."""
    url = reverse("tastecategories-delete", kwargs={"pk": create_tastecategory})
    response = api_client.delete(url)
    assert response.status_code == 401
    assert TasteCategories.objects.filter(id=create_tastecategory).exists()


@pytest.mark.django_db
def test_delete_tastecategory_with_token(api_client, get_token, create_tastecategory):
    """Тест удаления категории вкусов с токеном."""
    url = reverse("tastecategories-delete", kwargs={"pk": create_tastecategory})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not TasteCategories.objects.filter(id=create_tastecategory).exists()
