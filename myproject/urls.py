import os

from django.contrib import admin
from django.urls import include, path

version = "api/v1"

router_dir = os.path.join("api", "routers")

router_urls = [
    path(
        f"{version}/{r}/", include((f"api.routers.{r}", f"api-{r}"), namespace=f"api-{r}")
    )
    for router in os.listdir(router_dir)
    if router.endswith(".py")
    and not router.startswith("__")
    and (r := os.path.splitext(router)[0])
]

print(router_urls)

urlpatterns = [
    path("admin/", admin.site.urls),
] + router_urls
