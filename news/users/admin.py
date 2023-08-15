from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "role",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_editable = (
        "role",
        "is_staff",
    )
    search_fields = ("username",)
    empty_value_display = "-пусто-"
