from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    Serializer,
    CharField,
)
from .backends import WalletAuthenticationBackend
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class VerifySignatureSerializer(Serializer):
    wallet_address = CharField(max_length=42, write_only=True)
    signature = CharField(write_only=True)

    def save(self, **kwargs):
        """Updates existing or creates a new user and corresponding auth_session"""
        try:
            user = WalletAuthenticationBackend().authenticate(
                self.context["request"],
                wallet_address=self.validated_data["wallet_address"],
                signature=self.validated_data["signature"],
            )
        except Exception as e:
            print(e)
            raise AuthenticationFailed(str(e))
        return {"token": user.auth_session.auth_token}

