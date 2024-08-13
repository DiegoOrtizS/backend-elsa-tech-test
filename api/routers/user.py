from django.urls import path

from api.user.views import UserListView, UserView

urlpatterns = [
    path("user/", UserView.as_view(), name="user"),
    path("users/", UserListView.as_view({"get": "list"}), name="users"),
]
