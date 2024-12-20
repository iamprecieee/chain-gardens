from django.urls import path
from .views import GardenView, GardenStatusView, PlantTypeView, PlantManagementView


app_name = "gerden"

urlpatterns = [
    # Garden management
    path("", GardenView.as_view(), name="garden-detail"),
    path("status/", GardenStatusView.as_view(), name="system-status"),
    # Plant types
    path("plant-types/", PlantTypeView.as_view(), name="plant-types"),
    # Plant management
    path("plants/", PlantManagementView.as_view(), name="plant-create"),
    path("plants/<str:plant_id>/", PlantManagementView.as_view(), name="plant-delete"),
]
