from django.contrib.admin import register, ModelAdmin
from .models import User, UserAuthentication


@register(User)
class UserAdmin(ModelAdmin):
    list_display = [
        "id",
        "email",
        "wallet_address",
        "is_staff",
        "is_superuser",
        "is_active",
        "created",
        "updated",
        "last_login",
    ]
    list_filter = ["id", "is_staff", "is_superuser", "is_active", "created"]
    readonly_fields = ["id", "created"]


@register(UserAuthentication)
class UserAuthenticationAdmin(ModelAdmin):
    list_display = ["user", "auth_token", "created", "expiry", "is_valid"]
    list_filter = ["user", "is_valid", "created"]
    readonly_fields = ["user", "created"]
