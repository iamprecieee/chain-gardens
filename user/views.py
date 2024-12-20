from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import VerifySignatureSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .authentication import WalletTokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AuthenticateUserView(APIView):
    """Authenticates user with wallet signature"""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = VerifySignatureSerializer(
            data=request.data, context={"request": request}
        )
        try:
            if serializer.is_valid(raise_exception=True):
                response_data = serializer.save()
                return Response(
                    {"status": "success", "data": response_data},
                    status=status.HTTP_200_OK,
                )
        except (ValidationError, Exception) as e:
            return Response(
                {"status": "error", "error": str(e)},
                status=(
                    status.HTTP_400_BAD_REQUEST
                    if isinstance(e, ValidationError)
                    else status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )


class DisconnectUserView(APIView):
    """Disconnects user and invalidates auth token"""

    throttle_classess = [UserRateThrottle]

    def post(self, request):
        try:
            WalletTokenAuthentication().disconnect(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"status": "error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
