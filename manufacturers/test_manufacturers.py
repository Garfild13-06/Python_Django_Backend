import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from manufacturers.models import Manufacturers
from users.models import CustomUser


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    user = CustomUser.objects.create_user(
        email="user@example.com",
        username="testuser",
        password="password123",
    )
    return user


@pytest.fixture
def get_user_token(api_client, create_user):
    url = reverse("jwt-create")
    payload = {"email": "user@example.com", "password": "password123"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200
    return response.json()["data"]["access"]


@pytest.fixture
def create_manufacturer(db):
    manufacturer = Manufacturers.objects.create(
        name="Test Manufacturer",
        description="This is a test manufacturer",
    )
    return manufacturer


# ManufacturersListAPIView
@pytest.mark.django_db
def test_manufacturers_list_no_token(api_client, create_manufacturer):
    url = reverse("manufacturers-list")
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_manufacturers_list_with_token(api_client, get_user_token, create_manufacturer):
    url = reverse("manufacturers-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_manufacturers_list_pagination(api_client, create_manufacturer):
    url = reverse("manufacturers-list")
    payload = {"limit": 1, "offset": 0}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200


# ManufacturersDetailAPIView
@pytest.mark.django_db
def test_manufacturers_detail_no_token(api_client, create_manufacturer):
    url = reverse("manufacturers-detail", kwargs={"pk": str(create_manufacturer.id)})
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_manufacturers_detail_with_token(api_client, get_user_token, create_manufacturer):
    url = reverse("manufacturers-detail", kwargs={"pk": str(create_manufacturer.id)})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_manufacturers_detail_invalid_id(api_client):
    url = reverse("manufacturers-detail", kwargs={"pk": "123e4567-e89b-12d3-a456-426614174000"})
    response = api_client.post(url, format="json")
    assert response.status_code == 404


# ManufacturersCreateAPIView
@pytest.mark.django_db
def test_manufacturers_create_no_token(api_client):
    url = reverse("manufacturers-create")
    payload = {"name": "New Manufacturer", "description": "New Description"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_manufacturers_create_with_token(api_client, get_user_token):
    url = reverse("manufacturers-create")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"name": "New Manufacturer", "description": "New Description"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_manufacturers_create_missing_name(api_client, get_user_token):
    url = reverse("manufacturers-create")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"description": "Missing Name"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 400


# ManufacturersUpdateAPIView
@pytest.mark.django_db
def test_manufacturers_update_no_token(api_client, create_manufacturer):
    url = reverse("manufacturers-update", kwargs={"pk": str(create_manufacturer.id)})
    payload = {"name": "Updated Manufacturer", "description": "Updated Description"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_manufacturers_update_with_token(api_client, get_user_token, create_manufacturer):
    url = reverse("manufacturers-update", kwargs={"pk": str(create_manufacturer.id)})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"name": "Updated Manufacturer", "description": "Updated Description"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_manufacturers_update_invalid_id(api_client, get_user_token):
    url = reverse("manufacturers-update", kwargs={"pk": "123e4567-e89b-12d3-a456-426614174000"})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"name": "Invalid Update"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_manufacturers_update_missing_name(api_client, get_user_token, create_manufacturer):
    url = reverse("manufacturers-update", kwargs={"pk": str(create_manufacturer.id)})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"description": "No Name"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 400


# ManufacturersPartialUpdateAPIView
@pytest.mark.django_db
def test_manufacturers_partial_update_no_token(api_client, create_manufacturer):
    url = reverse("manufacturers-partial-update", kwargs={"pk": str(create_manufacturer.id)})
    payload = {"description": "Partially Updated"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_manufacturers_partial_update_with_token(api_client, get_user_token, create_manufacturer):
    url = reverse("manufacturers-partial-update", kwargs={"pk": str(create_manufacturer.id)})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"description": "Partially Updated"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_manufacturers_partial_update_invalid_id(api_client, get_user_token):
    url = reverse("manufacturers-partial-update", kwargs={"pk": "123e4567-e89b-12d3-a456-426614174000"})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"description": "Invalid Update"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 404


# ManufacturersDestroyAPIView
@pytest.mark.django_db
def test_manufacturers_delete_no_token(api_client, create_manufacturer):
    url = reverse("manufacturers-delete", kwargs={"pk": str(create_manufacturer.id)})
    response = api_client.delete(url, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_manufacturers_delete_with_token(api_client, get_user_token, create_manufacturer):
    url = reverse("manufacturers-delete", kwargs={"pk": str(create_manufacturer.id)})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    response = api_client.delete(url, format="json")
    assert response.status_code == 204


@pytest.mark.django_db
def test_manufacturers_delete_invalid_id(api_client, get_user_token):
    url = reverse("manufacturers-delete", kwargs={"pk": "123e4567-e89b-12d3-a456-426614174000"})
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    response = api_client.delete(url, format="json")
    assert response.status_code == 404
