from django.urls import path

from api.authentication.views import LoginRefreshView, LoginView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("login/refresh", LoginRefreshView.as_view(), name="login_refresh"),
]
