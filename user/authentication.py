"""
Wallet-based authentication system for Chain Gardens.
Implements secure token-based authentication with blockchain wallet verification.
"""

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .backends import WalletAuthenticationBackend


class WalletTokenAuthentication(BaseAuthentication):
    keyword = "Token"

    @staticmethod
    def retrieve_token(request, keyword):
        """Retrieves token from authorization header"""
        auth_header = get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != keyword.lower().encode("utf-8"):
            return None
        if len(auth_header) == 1:
            raise AuthenticationFailed("Invalid token header. No token provided.")
        elif len(auth_header) > 2:
            raise AuthenticationFailed(
                "Invalid token header. Token string contains spaces."
            )
        try:
            token = auth_header[1].decode("utf-8")
            return token
        except UnicodeError:
            raise AuthenticationFailed(
                "Invalid token header. Token string contains invalid characters."
            )
        except Exception as e:
            raise AuthenticationFailed(str(e))

    def authenticate(self, request):
        """
        Validates token using WalletAuthentication backend.
        Returns a user object and the token if valid.
        """
        token = self.retrieve_token(request, self.keyword)
        if token:
            user = WalletAuthenticationBackend().validate_auth_token(token)
            if user:
                return user, token
            raise AuthenticationFailed("Invalid or expired token.")
        return None

    def disconnect(self, request):
        """Invalidates token using WalletAuthentication backend"""
        token = self.retrieve_token(request, self.keyword)
        if token:
            WalletAuthenticationBackend.invalidate_auth_token(token)
        return None
