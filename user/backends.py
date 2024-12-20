from django.contrib.auth import get_user_model
from .models import UserAuthentication
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from eth_account.messages import encode_defunct
from web3 import Web3
from django.conf import settings
from django.db.transaction import atomic
from base.utils import generate_hex_token


User = get_user_model()

class WalletAuthenticationBackend:
    def authenticate(self, request, wallet_address=None, signature=None):
        """
        Authenticate a user using their wallet address and signature.
        Returns tuple of (user, auth_token) if successful, None otherwise.
        """
        try:
            if not wallet_address or not signature:
                raise AuthenticationFailed("Wallet address and signature required.")
            if not Web3.is_address(wallet_address):
                raise AuthenticationFailed("Invalid Ethereum address.")
            wallet_address = wallet_address.lower()
            # Generate a hash of a message equivalent to that which was signed
            message = f"Sign in to Chain Gardens with wallet: {wallet_address}"
            message_hash = encode_defunct(text=message)
            # Recover address from signature
            w3 = Web3()
            recovered_address = w3.eth.account.recover_message(
                message_hash, signature=signature
            )
            if recovered_address.lower() != wallet_address:
                raise AuthenticationFailed("Invalid signature.")
            with atomic():
                # Retrieve existing or create new user object
                user, _ = User.objects.get_or_create(wallet_address=wallet_address)
                user.last_login = timezone.now()
                user.save()
                # Invalidate any existing sessions for security
                if hasattr(user, "auth_session"):
                    user.auth_session.auth_token = generate_hex_token()
                    user.auth_session.expiry = timezone.now() + timezone.timedelta(seconds=settings.AUTH_TOKEN_EXPIRY)
                    user.auth_session.save()
                else:
                    # Create new authentication session
                    UserAuthentication.objects.create(
                        user=user,
                        expiry=timezone.now()
                        + timezone.timedelta(seconds=settings.AUTH_TOKEN_EXPIRY),
                    )
                return user
        except Exception as e:
            raise AuthenticationFailed("Authentication failed: " + str(e))
    
    @staticmethod
    def validate_auth_token(auth_token):
        """
        Validates a given auth token against that stored in db.
        Returns the corresponding user object if token is valid.
        """
        auth_session = (
            UserAuthentication.objects.select_related("user")
            .filter(auth_token=auth_token, expiry__gt=timezone.now())
            .first()
        )
        return auth_session.user if auth_session else None

    @staticmethod
    def invalidate_auth_token(auth_token):
        """Invalidates an authentication token."""
        UserAuthentication.objects.filter(auth_token=auth_token).delete()
