from users.models import User
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
