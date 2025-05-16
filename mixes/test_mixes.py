import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from mixes.models import Mixes, MixLikes, MixFavorites
from users.models import CustomUser


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API."""
    return APIClient()


@pytest.fixture
def create_user():
    """Фикстура для создания тестового пользователя."""
    user = CustomUser.objects.create_user(
        email="testuser@example.com",
        username="testuser",
        password="password123",
    )
    return user


@pytest.fixture
def get_token(api_client, create_user):
    """Фикстура для получения JWT-токена."""
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
def create_mix(create_user):
    """Фикстура для создания тестового микса."""
    mix = Mixes.objects.create(
        name="Test Mix",
        description="This is a test mix",
        banner=None,
        tasteType="fruit",
        author=create_user,
    )
    return mix


# Тесты для создания микса
@pytest.mark.django_db
def test_create_mix_no_token(api_client):
    """Тест создания микса без токена."""
    url = reverse("mix-create")
    payload = {
        "name": "New Mix",
        "description": "New Description",
        "tasteType": "fruit",
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_mix_with_token(api_client, get_token, create_user):
    """Тест создания микса с токеном."""
    url = reverse("mix-create")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {
        "name": "New Mix",
        "description": "New Description",
        "tasteType": "fruit",
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201
    assert Mixes.objects.filter(name="New Mix").exists()


# Тесты для получения списка миксов
@pytest.mark.django_db
def test_list_mixes_no_token(api_client, create_mix):
    """Тест получения списка миксов без токена."""
    url = reverse("mixes-list")
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


@pytest.mark.django_db
def test_list_mixes_with_token(api_client, get_token, create_mix):
    """Тест получения списка миксов с токеном."""
    url = reverse("mixes-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


@pytest.mark.django_db
def test_list_mixes_with_search(api_client, create_mix):
    """Тест получения списка миксов с использованием поиска."""
    url = reverse("mixes-list")
    search_query = {"search": "Test"}  # Поиск по ключевому слову "Test"
    response = api_client.post(url, data=search_query, format="json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0  # Убедимся, что есть хотя бы один результат
    print(data)
    assert any("Test" in mix["name"] for mix in data["results"])  # Проверяем, что результат содержит искомое слово


# Тесты для получения деталей микса
@pytest.mark.django_db
def test_retrieve_mix_no_token(api_client, create_mix):
    """Тест получения деталей микса без токена."""
    url = reverse("mix-detail")
    data = {"id": str(create_mix.id)}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Test Mix"


@pytest.mark.django_db
def test_retrieve_mix_invalid_id(api_client):
    """Тест получения несуществующего микса."""
    url = reverse("mix-detail")
    data = {"id": "ffffffff-ffff-ffff-ffff-ffffffffffff"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 404


# Тесты для обновления микса
@pytest.mark.django_db
def test_update_mix_no_token(api_client, create_mix):
    """Тест полного обновления микса без токена."""
    url = reverse("mix-update")
    payload = {
        "mix_id": str(create_mix),
        "name": "Updated Mix",
        "description": "Updated Description",
    }
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_mix_with_token(api_client, get_token, create_mix):
    """Тест полного обновления микса с токеном."""
    url = reverse("mix-update")  # URL без параметров
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {
        "mix_id": str(create_mix.id),
        "name": "Updated Mix",
        "description": "Updated Description",
    }
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 200
    updated_mix = Mixes.objects.get(id=create_mix.id)
    assert updated_mix.name == "Updated Mix"


# Тесты для удаления микса
@pytest.mark.django_db
def test_delete_mix_no_token(api_client, create_mix):
    """Тест удаления микса без токена."""
    url = reverse("mix-delete")
    payload = {"mix_id": str(create_mix.id)}
    response = api_client.delete(url, data=payload, format="json")
    assert response.status_code == 401
    assert Mixes.objects.filter(id=create_mix.id).exists()


@pytest.mark.django_db
def test_delete_mix_with_token(api_client, get_token, create_mix):
    """Тест удаления микса с токеном."""
    url = reverse("mix-delete")
    payload = {"mix_id": str(create_mix.id)}
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    response = api_client.delete(url, data=payload, format="json")
    assert response.status_code == 204
    assert not Mixes.objects.filter(id=create_mix.id).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "setup_like, expected_action",
    [
        (False, "liked"),  # Если лайка нет → добавляем
        (True, "unliked"),  # Если лайк есть → удаляем
    ]
)
def test_like_unlike_mix(api_client, get_token, create_mix, create_user, setup_like, expected_action):
    """Тест добавления и удаления лайка к миксу."""
    if setup_like:
        MixLikes.objects.create(mix=create_mix, user=create_user)

    url = reverse("mix-like")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {"mix_id": str(create_mix.id)}
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["data"]["action"] == expected_action


@pytest.mark.django_db
@pytest.mark.parametrize(
    "setup_like, expected_action",
    [
        (False, "favorited"),  # Если лайка нет → добавляем
        (True, "disfavorited"),  # Если лайк есть → удаляем
    ]
)
def test_favorited_disfavorite_mix(api_client, get_token, create_mix, create_user, setup_like, expected_action):
    """Тест добавления и удаления лайка к миксу."""
    if setup_like:
        MixFavorites.objects.create(mix=create_mix, user=create_user)

    url = reverse("mix-favorite")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access']}")
    payload = {"mix_id": str(create_mix.id)}
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["data"]["action"] == expected_action
