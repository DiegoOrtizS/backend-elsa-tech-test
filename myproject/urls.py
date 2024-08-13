import os

from django.contrib import admin
from django.urls import include, path

version = "api/v1"

router_dir = os.path.join("api", "routers")

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{version}/auth/", include("api.routers.auth")),
    path(f"{version}/", include("api.routers.user")),
    path(f"{version}/", include("api.routers.animal")),
]
