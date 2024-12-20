from django.urls import path
from .views import AuthenticateUserView, DisconnectUserView


app_name = "user"

urlpatterns = [
    path("authenticate/", AuthenticateUserView.as_view(), name="authenticate-user"),
    path("disconnect/", DisconnectUserView.as_view(), name="disconnect-user"),
]
