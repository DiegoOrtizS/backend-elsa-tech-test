from django.urls import path

from api.user.views import UserListView, UserView

urlpatterns = [
    path("users/", UserListView.as_view({"get": "list"}), name="users"),
    path("user/<uuid:id>/", UserView.as_view(), name="user"),
    path("user/", UserView.as_view(), name="user"),
]
