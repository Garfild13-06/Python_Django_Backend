import pytest
from django.urls import reverse
from rest_framework.test import APIClient
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
def create_admin(db):
    admin = CustomUser.objects.create_superuser(
        email="admin@example.com",
        username="adminuser",
        password="admin123",
    )
    return admin


@pytest.fixture
def get_user_token(api_client, create_user):
    url = reverse("jwt-create")
    payload = {"email": "user@example.com", "password": "password123"}
    response = api_client.post(url, data=payload, format="json")
    return response.json()["data"]["access"]


@pytest.fixture
def get_admin_token(api_client, create_admin):
    url = reverse("jwt-create")
    payload = {"email": "admin@example.com", "password": "admin123"}
    response = api_client.post(url, data=payload, format="json")
    return response.json()["data"]["access"]


# UserListAPIView
@pytest.mark.django_db
def test_user_list_no_token(api_client):
    url = reverse("user-list")
    response = api_client.post(url, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_list_user_token(api_client, get_user_token, create_user):
    url = reverse("user-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    response = api_client.post(url, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_list_admin_token(api_client, get_admin_token, create_user):
    url = reverse("user-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_admin_token}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_list_filter_by_email(api_client, get_admin_token, create_user):
    url = reverse("user-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_admin_token}")
    payload = {"email": "user@example.com"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_list_pagination(api_client, get_admin_token, create_user):
    url = reverse("user-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_admin_token}")
    payload = {"limit": 1, "offset": 0}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200


# UserDetailAPIView
@pytest.mark.django_db
def test_user_detail_no_token(api_client, create_user):
    url = reverse("user-detail")
    payload = {"id": str(create_user.id)}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_detail_owner_token(api_client, get_user_token, create_user):
    url = reverse("user-detail")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"id": str(create_user.id)}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_detail_admin_token(api_client, get_admin_token, create_user):
    url = reverse("user-detail")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_admin_token}")
    payload = {"id": str(create_user.id)}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_detail_other_user(api_client, get_user_token, create_admin):
    url = reverse("user-detail")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"id": str(create_admin.id)}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 403


# UserCreateAPIView
@pytest.mark.django_db
def test_user_create_valid(api_client):
    url = reverse("user-create")
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpass123"
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_create_missing_fields(api_client):
    url = reverse("user-create")
    payload = {"email": "newuser@example.com"}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_create_duplicate_email(api_client, create_user):
    url = reverse("user-create")
    payload = {
        "email": "user@example.com",
        "username": "newuser2",
        "password": "newpass123"
    }
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 400


# UserUpdateAPIView
@pytest.mark.django_db
def test_user_update_no_token(api_client, create_user):
    url = reverse("user-update")
    payload = {"id": str(create_user.id), "username": "updateduser"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_update_owner(api_client, get_user_token, create_user):
    url = reverse("user-update")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"id": str(create_user.id), "username": "updateduser"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_admin(api_client, get_admin_token, create_user):
    url = reverse("user-update")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_admin_token}")
    payload = {"id": str(create_user.id), "username": "adminupdated"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_update_other_user(api_client, get_user_token, create_admin):
    url = reverse("user-update")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"id": str(create_admin.id), "username": "hacked"}
    response = api_client.put(url, data=payload, format="json")
    assert response.status_code == 403


# UserPartialUpdateAPIView
@pytest.mark.django_db
def test_user_partial_update_owner(api_client, get_user_token, create_user):
    url = reverse("user-partial-update")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"id": str(create_user.id), "nickname": "NewNick"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_partial_update_admin(api_client, get_admin_token, create_user):
    url = reverse("user-partial-update")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_admin_token}")
    payload = {"id": str(create_user.id), "nickname": "AdminNick"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_partial_update_no_id(api_client, get_user_token):
    url = reverse("user-partial-update")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"nickname": "NoID"}
    response = api_client.patch(url, data=payload, format="json")
    assert response.status_code == 400


# UserDeleteAPIView
@pytest.mark.django_db
def test_user_delete_no_token(api_client, create_user):
    url = reverse("user-delete")
    payload = {"id": str(create_user.id)}
    response = api_client.delete(url, data=payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_delete_admin(api_client, get_admin_token, create_user):
    url = reverse("user-delete")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_admin_token}")
    payload = {"id": str(create_user.id)}
    response = api_client.delete(url, data=payload, format="json")
    assert response.status_code == 204


@pytest.mark.django_db
def test_user_delete_user(api_client, get_user_token, create_user):
    url = reverse("user-delete")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    payload = {"id": str(create_user.id)}
    response = api_client.delete(url, data=payload, format="json")
    assert response.status_code == 403


# UserProfileView
@pytest.mark.django_db
def test_user_profile_no_token(api_client):
    url = reverse("user-profile")
    response = api_client.post(url, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_profile_valid_token(api_client, get_user_token, create_user):
    url = reverse("user-profile")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_user_token}")
    response = api_client.post(url, format="json")
    assert response.status_code == 200
