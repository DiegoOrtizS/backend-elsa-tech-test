from typing import TypedDict

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from typing_extensions import Unpack


class UserKwargs(TypedDict, total=False):
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool


class CustomUserManager(BaseUserManager):
    """
    Custom user manager class
    """

    def create(
        self, email: str, password: str | None = None, **kwargs: Unpack[UserKwargs]
    ) -> "CustomUser":
        """
        Create and return a regular user with an email and password

        Args:
        -----
            email (str): user email
            password (str): user password
            **kwargs: additional fields

        Returns:
        --------
            CustomUser: user object

        Raises:
        -------
            ValueError: if email is not set
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user: CustomUser = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **kwargs: Unpack[UserKwargs]
    ) -> "CustomUser":
        """
        Create and return a superuser with an email and password

        Args:
        -----
            email (str): user email
            password (str): user password
            **kwargs: additional fields

        Returns:
        --------
            CustomUser: user object

        Raises:
        -------
            ValueError: if email is not set
        """

        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        return self.create(email, password, **kwargs)


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()

    def __str__(self) -> str:
        return str(self.email)


class UserProfile(models.Model):
    """
    User profile model

    Attributes:
    -----------
        user (CustomUser): user object
        role (str): user role
    """

    USER_ROLES = [
        ("volunteer", "Volunteer"),
        ("adopter", "Adopter"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    objects = models.Manager()
