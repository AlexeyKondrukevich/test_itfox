from django.urls import include, path
from rest_framework import routers

from .views import (
    APIObtainToken,
    CommentViewSet,
    NewsViewSet,
    SignUp,
    UsersViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register(r"users", UsersViewSet, basename="users")
router.register(r"news", NewsViewSet, basename="news")
router.register(
    r"news/(?P<news_id>\d+)/comments",
    CommentViewSet,
    basename="reviews",
)

urlpatterns = [
    path("v1/auth/signup/", SignUp.as_view(), name="signup"),
    path("v1/auth/token/", APIObtainToken.as_view(), name="obtain_token"),
    path("v1/", include(router.urls)),
]
