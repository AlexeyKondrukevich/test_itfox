from rest_framework import serializers

from comments.models import Comment, News
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        )


# class ConfirmationCodeSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     confirmation_code = serializers.SerializerMethodField()
# confirmation_code = serializers.SerializerMethodField()

# class Meta:
#     model = User
#     fields = ("username", "email", "confirmation_code")
#     read_only = ("confirmation_code",)

# def get_confirmation_code(self, obj):
# serializer = ConfirmationCodeSerializer()
# serializer.is_valid(raise_exception=True)
# username = serializer.validated_data.get("username")
# email = serializer.validated_data.get("email")
# user = get_object_or_404(User, username=username)
# return obj.confirmation_code


class SingUpSerializer(serializers.ModelSerializer):
    # confirmation_code = serializers.SerializerMethodField()
    # confirmation_code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        # fields = ("username", "email", "confirmation_code")
        fields = (
            "username",
            "email",
        )
        # read_only = ("confirmation_code",)

    def create(self, validated_data):
        user = User.objects.create(
            username=self.validated_data["username"],
            email=self.validated_data["email"],
        )
        return user

    # def get_confirmation_code(self, obj):
    # serializer = ConfirmationCodeSerializer()
    # serializer.is_valid(raise_exception=True)
    # username = serializer.validated_data.get("username")
    # email = serializer.validated_data.get("email")
    # user = get_object_or_404(User, username=username)
    # return obj.confirmation_code

    # def to_representation(self, instance):
    #     return ConfirmationCodeSerializer(instance).data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
        )

    @staticmethod
    def get_full_name(obj):
        return obj.get_full_name()


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    comments_amount = serializers.SerializerMethodField()
    latest_comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            "id",
            "author",
            "text",
            "pub_date",
            "comments_amount",
            "latest_comments",
            "likes",
        )

    def get_comments_amount(self, obj):
        return obj.comments.count()

    def get_latest_comments(self, obj):
        comments = Comment.objects.filter(news=obj).order_by("pub_date")[:10]
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_likes(self, obj):
        return obj.total_likes


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only = ("id",)
