from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models import (
    Model,
    CharField,
    EmailField,
    BooleanField,
    DateTimeField,
    OneToOneField,
    CASCADE,
)
from base.utils import generate_id, generate_hex_token


class CustomUserManager(BaseUserManager):
    def _create_user(self, **kwargs):
        from django.db.transaction import atomic

        with atomic():
            user = self.model(**kwargs)
            if kwargs.get("is_superuser"):
                user.email = self.normalize_email(kwargs.get("email"))
                user.set_password(kwargs.get("password"))
            else:
                user.wallet_address = kwargs.get("wallet_address").lower()
            user.save(using=self._db)
            return user
        raise Exception("User creation failed. Review data and try again.")

    def create_user(self, **kwargs):
        """Creates a regular user with wallet address only"""
        kwargs.pop("email", None)
        kwargs.pop("password", None)
        if not kwargs.get("wallet_address"):
            raise ValueError("Wallet address is required for regular users.")
        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs):
        """Creates a superuser with email and password"""
        kwargs.pop("wallet_address", None)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        if any([not kwargs.get("email"), not kwargs.get("password")]):
            raise ValueError("Email and password are required for superusers.")
        return self._create_user(**kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    id = CharField(
        max_length=21,
        primary_key=True,
        editable=False,
        unique=True,
        default=generate_id,
    )
    email = EmailField(blank=True, null=True, unique=True)
    wallet_address = CharField(max_length=42, blank=True, null=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    last_login = DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return f"User {self.wallet_address}" if self.wallet_address else str(self.email)

    @property
    def get_short_address(self):
        return (
            f"{self.wallet_address[:6]}...{self.wallet_address[-4:]}"
            if self.wallet_address
            else None
        )

    class Meta:
        db_table = "user"
        ordering = ["-created"]


class UserAuthentication(Model):
    """Stores a user's authentication data e.g. auth token, token expiry"""

    user = OneToOneField(User, on_delete=CASCADE, related_name="auth_session")
    auth_token = CharField(
        max_length=64, default=generate_hex_token, unique=True)
    is_valid = BooleanField(default=True)
    created = DateTimeField(auto_now_add=True)
    expiry = DateTimeField()

    def __str__(self):
        return f"{self.user}'s auth session"
