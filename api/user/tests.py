from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.user.models import CustomUser, UserProfile


@pytest.fixture
def admin_user() -> CustomUser:
    return CustomUser.objects.create_superuser(
        email="admin@example.com", password="admin123"
    )


@pytest.fixture
def client(admin_user: CustomUser) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def user() -> CustomUser:
    return CustomUser.objects.create(email="testuser@example.com", password="password123")


@pytest.fixture
def user_profile(user: CustomUser) -> UserProfile:
    return UserProfile.objects.create(user=user, role="volunteer")


@pytest.mark.parametrize(
    "data,expected_status_code",
    [
        (
            {
                "user": {"email": "test@example.com", "password": "pass123"},
                "role": "adopter",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {"user": {"email": "test@example.com", "password": ""}, "role": "adopter"},
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {"user": {"email": "", "password": "pass123"}, "role": "adopter"},
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "user": {"email": "test@example.com", "password": "testpass123"},
                "role": "test",
            },
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            {
                "user": {"email": "test@example.com", "password": "testpass123"},
                "role": "adopter",
            },
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.django_db
def test_create_user_with_various_data(
    client: APIClient, data: dict, expected_status_code: int
) -> None:
    url = reverse("user")
    response = client.post(url, data, format="json")
    assert response.status_code == expected_status_code


@pytest.mark.django_db
def test_get_user_profile(client: APIClient, user_profile: UserProfile) -> None:
    url = reverse("user", kwargs={"id": user_profile.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["role"] == user_profile.role


@pytest.mark.django_db
def test_update_user_profile(client: APIClient, user_profile: UserProfile) -> None:
    url = reverse("user", kwargs={"id": user_profile.id})
    data = {"role": "adopter"}
    response = client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    user_profile.refresh_from_db()
    assert user_profile.role == "adopter"


@pytest.mark.django_db
def test_delete_user_profile(client: APIClient, user_profile: UserProfile) -> None:
    url = reverse("user", kwargs={"id": user_profile.id})
    response = client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert UserProfile.objects.count() == 0


@pytest.mark.parametrize(
    "role,expected_count",
    [
        ("", 1),
        ("volunteer", 1),
        ("adopter", 0),
    ],
)
@pytest.mark.django_db
def test_list_user_profiles(
    client: APIClient,
    user_profile: UserProfile,  # noqa: ARG001
    role: str,
    expected_count: int,
) -> None:
    url = reverse("users")
    response = client.get(url, {"role": role})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_count


@pytest.mark.parametrize(
    "method,expected_status_code",
    [
        ("get", status.HTTP_404_NOT_FOUND),
        ("patch", status.HTTP_404_NOT_FOUND),
        ("delete", status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.django_db
def test_user_profile_not_found(
    client: APIClient, method: str, expected_status_code: int
) -> None:
    non_existent_uuid = uuid4()
    url = reverse("user", kwargs={"id": non_existent_uuid})

    if method == "get":
        response = client.get(url)
    elif method == "patch":
        data = {"role": "adopter"}
        response = client.patch(url, data, format="json")
    elif method == "delete":
        response = client.delete(url)
    else:
        pytest.fail(f"Unsupported method: {method}")

    assert response.status_code == expected_status_code
