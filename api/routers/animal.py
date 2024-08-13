from django.urls import path

from api.animal.views import AnimalListView, AnimalView

urlpatterns = [
    path("animals/", AnimalListView.as_view({"get": "list"}), name="animals"),
    path("animal/<uuid:id>/", AnimalView.as_view(), name="animal"),
    path("animal/", AnimalView.as_view(), name="animal"),
]
