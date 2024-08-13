from django.urls import path

from api.adoption.views import AdoptionListView, AdoptionView

urlpatterns = [
    path("adoptions/", AdoptionListView.as_view({"get": "list"}), name="adoptions"),
    path("adoption/<uuid:id>/", AdoptionView.as_view(), name="adoption"),
    path("adoption/", AdoptionView.as_view(), name="adoption"),
]
