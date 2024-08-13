from uuid import uuid4

from django.db import models

from api.animal.models import Animal
from api.user.models import CustomUser


class Adoption(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("finalized", "Finalized"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="adoptions")
    volunteer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="volunteer_adoptions",
    )
    adopter = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="adopter_adoptions"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="in_progress"
    )

    def __str__(self) -> str:
        return f"Adoption of {self.animal.name} by {self.adopter.username} on {self.date}"
