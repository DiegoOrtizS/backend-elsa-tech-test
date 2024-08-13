from uuid import uuid4

from django.db import models


class Animal(models.Model):
    PET_TYPE_CHOICES = [
        ("dog", "Dog"),
        ("cat", "Cat"),
    ]

    STATUS_CHOICES = [
        ("adopted", "Adopted"),
        ("available", "Available for Adoption"),
        ("pending", "Pending Adoption"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.name} ({self.get_pet_type_display()})"
