from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .mixins import LikedMixin
from .permissions import IsAdmin
from .serializers import (
    CommentSerializer,
    ConfirmationCodeSerializer,
    GetTokenSerializer,
    NewsSerializer,
    SingUpSerializer,
    UserSerializer,
)
from comments.models import Comment, News
from news.settings import DEFAULT_FROM_EMAIL
from users.models import User


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdmin,)
    # pagination_class = PageNumberPagination
    lookup_field = "username"


def sent_confirmation_code(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    email = serializer.validated_data.get("email")
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    return send_mail(
        "Код подтверждения",
        f"Ваш код подтверждения: {confirmation_code}",
        [DEFAULT_FROM_EMAIL],
        [email],
        fail_silently=False,
    )


class SignUp(APIView):
    queryset = User.objects.all()
    serializer_class = SingUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sent_confirmation_code(request)
        return Response(request.data, status=status.HTTP_200_OK)


class APIObtainToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get("confirmation_code")
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response(
            {"confirmation_code": "Неверный код подтверждения!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class NewsViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # permission_classes = (
    #     IsAuthenticated,
    #     AuthorModeratorOrReadOnly,
    # )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.filter(news_id=self.kwargs.get("news_id"))
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, news_id=self.kwargs.get("news_id")
        )
