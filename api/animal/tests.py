from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.test import APIClient

from api.animal.models import Animal
from api.user.models import CustomUser, UserProfile


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def admin_user() -> CustomUser:
    user = CustomUser.objects.create_superuser(email="admin", password="admin")
    return user


@pytest.fixture
def volunteer_user() -> CustomUser:
    user = CustomUser.objects.create(email="volunteer", password="volunteer")
    UserProfile.objects.create(user=user, role="volunteer")
    return user


@pytest.fixture
def adopter_user() -> CustomUser:
    user = CustomUser.objects.create(email="adopter", password="adopter")
    UserProfile.objects.create(user=user, role="adopter")
    return user


@pytest.fixture
def animal() -> Animal:
    return Animal.objects.create(
        name="Catilin", age=1, breed="chusca", pet_type="cat", status="pending"
    )


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("admin_user", status.HTTP_201_CREATED),
        ("volunteer_user", status.HTTP_403_FORBIDDEN),
        ("adopter_user", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_create_animal(
    api_client: APIClient, user_fixture: str, expected_status: int, request: Request
) -> None:
    user: CustomUser = request.getfixturevalue(user_fixture)
    api_client.force_authenticate(user=user)

    url: str = reverse("animal")
    data: dict[str, str | int] = {
        "name": "Fluffy",
        "age": 2,
        "breed": "chusco",
        "pet_type": "dog",
        "status": "available",
    }
    response = api_client.post(url, data)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("admin_user", status.HTTP_200_OK),
        ("volunteer_user", status.HTTP_403_FORBIDDEN),
        ("adopter_user", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_get_animal(
    api_client: APIClient,
    animal: Animal,
    user_fixture: str,
    expected_status: int,
    request: Request,
) -> None:
    user: CustomUser = request.getfixturevalue(user_fixture)
    api_client.force_authenticate(user=user)

    url: str = reverse("animal", kwargs={"id": animal.id})
    response = api_client.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("admin_user", status.HTTP_200_OK),
        ("volunteer_user", status.HTTP_403_FORBIDDEN),
        ("adopter_user", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_delete_animal(
    api_client: APIClient,
    animal: Animal,
    user_fixture: str,
    expected_status: int,
    request: Request,
) -> None:
    user: CustomUser = request.getfixturevalue(user_fixture)
    api_client.force_authenticate(user=user)

    url: str = reverse("animal", kwargs={"id": animal.id})
    response = api_client.delete(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("admin_user", status.HTTP_200_OK),
        ("adopter_user", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_patch_animal(
    api_client: APIClient,
    animal: Animal,
    user_fixture: str,
    expected_status: int,
    request: Request,
) -> None:
    user: CustomUser = request.getfixturevalue(user_fixture)
    api_client.force_authenticate(user=user)

    url: str = reverse("animal", kwargs={"id": animal.id})
    data: dict[str, str] = {"status": "adopted"}
    response = api_client.patch(url, data)

    assert response.status_code == expected_status
    if response.status_code == status.HTTP_200_OK:
        animal.refresh_from_db()
        assert animal.status == data["status"]


@pytest.mark.parametrize(
    "user_fixture, expected_status, expected_count",
    [
        ("admin_user", status.HTTP_200_OK, 1),
        ("volunteer_user", status.HTTP_200_OK, 1),
        ("adopter_user", status.HTTP_200_OK, 0),
    ],
)
@pytest.mark.django_db
def test_list_animals(
    api_client: APIClient,
    animal: Animal,  # noqa: ARG001
    user_fixture: str,
    expected_status: int,
    expected_count: int,
    request: Request,
) -> None:
    user: CustomUser = request.getfixturevalue(user_fixture)
    api_client.force_authenticate(user=user)

    url: str = reverse("animals")
    response = api_client.get(url)

    assert response.status_code == expected_status
    assert response.data["count"] == expected_count


@pytest.mark.parametrize(
    "method,expected_status_code",
    [
        ("get", status.HTTP_404_NOT_FOUND),
        ("patch", status.HTTP_404_NOT_FOUND),
        ("delete", status.HTTP_404_NOT_FOUND),
    ],
)
@pytest.mark.django_db
def test_animal_not_found(
    api_client: APIClient, admin_user: CustomUser, method: str, expected_status_code: int
) -> None:
    non_existent_uuid = uuid4()
    api_client.force_authenticate(user=admin_user)
    url = reverse("animal", kwargs={"id": non_existent_uuid})

    if method == "get":
        response = api_client.get(url)
    elif method == "patch":
        data = {"status": "adopted"}
        response = api_client.patch(url, data, format="json")
    elif method == "delete":
        response = api_client.delete(url)
    else:
        pytest.fail(f"Unsupported method: {method}")

    assert response.status_code == expected_status_code
