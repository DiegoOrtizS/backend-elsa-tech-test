from django.urls import path

from api.user.views import UserView

urlpatterns = [
    path("", UserView.as_view(), name="user"),
]
