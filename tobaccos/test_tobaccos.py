import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tobaccos.models import Tobaccos
from manufacturers.models import Manufacturers


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    """Создание тестового пользователя."""
    from users.models import CustomUser
    user = CustomUser.objects.create_user(
        email="testuser@example.com",
        username="testuser",
        password="password123",
    )
    return user


@pytest.fixture
def get_token(api_client, create_user):
    """Получение JWT-токена для зарегистрированного пользователя."""
    url = reverse("jwt-create")
    payload = {
        "email": create_user.email,
        "password": "password123",
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200
    return {
        "access": response.json()["data"]["access"],
        "refresh": response.json()["data"]["refresh"],
    }


@pytest.fixture
def create_manufacturer():
    """Создание тестового производителя."""
    manufacturer = Manufacturers.objects.create(
        name="Test Manufacturer",
        description="Test Description",
    )
    return manufacturer


@pytest.fixture
def create_tobacco(create_manufacturer):
    """Создание тестового табака."""
    tobacco = Tobaccos.objects.create(
        taste="Test Taste",
        manufacturer=create_manufacturer,
        description="Test Description",
        tobacco_strength="5",
        tobacco_resistance="middle",
        tobacco_smokiness="high",
    )
    return tobacco


# Тесты для получения списка табаков
@pytest.mark.django_db
def test_tobacco_list_without_token(api_client, create_tobacco):
    """Тест получения списка табаков без токена."""
    url = reverse("tobaccos-list")  # Предположим, что URL называется 'tobaccos-list'
    response = api_client.post(url, data={}, format="json")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


@pytest.mark.django_db
def test_tobacco_list_with_search(api_client, create_tobacco):
    """Тест поиска табаков."""
    url = reverse("tobaccos-list")
    search_query = {"search": "Test"}  # Ensure this matches the taste of the created tobacco
    response = api_client.post(url, data=search_query, format="json")
    assert response.status_code == 200
    data = response.json()["data"]["results"]
    assert len(data) > 0  # Ensure at least one result is returned
    assert "Test" in data[0]["taste"]  # Verify the search result contains the expected taste


@pytest.mark.django_db
def test_tobacco_list_with_pagination(api_client, create_tobacco):
    """Тест пагинации."""
    url = reverse("tobaccos-list")
    pagination_query = {"limit": 1, "offset": 0}
    response = api_client.post(url, data=pagination_query, format="json")
    assert response.status_code == 200
    data = response.json()["data"]["results"]
    assert len(data) == 1  # Ensure only one item is returned


# Тесты для получения деталей табака
@pytest.mark.django_db
def test_tobacco_detail_without_token(api_client, create_tobacco):
    """Тест получения деталей табака без токена."""
    url = reverse("tobaccos-detail")
    data = {"id": str(create_tobacco.id)}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 200
    assert response.json()["data"]["taste"] == "Test Taste"


@pytest.mark.django_db
def test_tobacco_detail_invalid_id(api_client):
    """Тест получения деталей несуществующего табака."""
    url = reverse("tobaccos-detail")
    data = {"id": "ffffffff-ffff-ffff-ffff-ffffffffffff"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 404


# Тесты для создания табака
@pytest.mark.django_db
def test_create_tobacco_with_token(api_client, get_token, create_manufacturer):
    """Тест создания табака с токеном."""
    url = reverse("tobaccos-create")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    data = {
        "taste": "New Tobacco",
        "manufacturer": str(create_manufacturer.id),
        "description": "New Description",
        "tobacco_strength": "7",
        "tobacco_resistance": "low",
        "tobacco_smokiness": "medium",
    }
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 201
    assert response.json()["data"]["taste"] == "New Tobacco"


@pytest.mark.django_db
def test_create_tobacco_without_token(api_client, create_manufacturer):
    """Тест создания табака без токена."""
    url = reverse("tobaccos-create")
    data = {
        "taste": "New Tobacco",
        "manufacturer": str(create_manufacturer.id),
        "description": "New Description",
        "tobacco_strength": "7",
        "tobacco_resistance": "low",
        "tobacco_smokiness": "medium",
    }
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 401


# Тесты для обновления табака
@pytest.mark.django_db
def test_update_tobacco_with_token(api_client, get_token, create_tobacco):
    """Тест полного обновления табака с токеном."""
    url = reverse("tobaccos-update", kwargs={"pk": create_tobacco.id})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    data = {
        "taste": "Updated Taste",
        "manufacturer": str(create_tobacco.manufacturer.id),
        "description": "Updated Description",
        "tobacco_strength": "8",
        "tobacco_resistance": "high",
        "tobacco_smokiness": "low",
    }
    response = api_client.put(url, data=data, format="json")
    assert response.status_code == 200
    assert response.json()["data"]["taste"] == "Updated Taste"


@pytest.mark.django_db
def test_partial_update_tobacco_with_token(api_client, get_token, create_tobacco):
    """Тест частичного обновления табака с токеном."""
    url = reverse("tobaccos-partial-update", kwargs={"pk": create_tobacco.id})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    data = {"taste": "Partially Updated Taste"}
    response = api_client.patch(url, data=data, format="json")
    assert response.status_code == 200
    assert response.json()["data"]["taste"] == "Partially Updated Taste"


# Тесты для удаления табака
@pytest.mark.django_db
def test_delete_tobacco_with_token(api_client, get_token, create_tobacco):
    """Тест удаления табака с токеном."""
    url = reverse("tobaccos-delete", kwargs={"pk": create_tobacco.id})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Tobaccos.objects.filter(id=create_tobacco.id).exists()


@pytest.mark.django_db
def test_delete_tobacco_without_token(api_client, create_tobacco):
    """Тест удаления табака без токена."""
    url = reverse("tobaccos-delete", kwargs={"pk": create_tobacco.id})
    response = api_client.delete(url)
    assert response.status_code == 401
