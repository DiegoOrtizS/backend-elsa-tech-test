import os

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

version = "api/v1"

router_dir = os.path.join("api", "routers")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{version}/auth/", include("api.routers.auth")),
    path(f"{version}/", include("api.routers.user")),
    path(f"{version}/", include("api.routers.animal")),
    path(f"{version}/", include("api.routers.adoption")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
