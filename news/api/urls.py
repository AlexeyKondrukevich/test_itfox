from django.urls import include, path
from rest_framework import routers
from .views import UsersViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("users", UsersViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
]
