from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Garden, PlantType, Plant
from .serializers import GardenSerializer, PlantTypeSerializer, PlantSerializer


class GardenView(APIView):
    """Get or create a user's garden"""

    def get(self, request):
        try:
            garden, created = Garden.objects.get_or_create(owner=request.user)
            response_data = GardenSerializer(garden).data
            return Response(
                {"success": True, "data": response_data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "error": f"Garden retrieval failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GardenStatusView(APIView):
    """Monitor system status and recent updates"""

    def get(self, request):
        """Get current garden status"""
        from blockchain.models import WeatherState
        from blockchain.serializers import WeatherStateSerializer

        try:
            garden = request.user.garden
            current_weather = WeatherState.objects.last()
            garden_data = GardenSerializer(garden).data
            weather_data = (
                WeatherStateSerializer(current_weather).data
                if current_weather
                else None
            )
            return Response(
                {
                    "status": "success",
                    "data": {"garden_data": garden_data, "weather_data": weather_data},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "error": f"Garden status retrieval failed: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlantTypeView(APIView):
    def get(self, request):
        """Get available plant types"""
        try:
            plant_types = PlantType.objects.all()
            plant_types_data = PlantTypeSerializer(plant_types, many=True).data
            return Response(
                {
                    "status": "success",
                    "data": {"plant_types_data": plant_types_data},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "error": f"Plant types retrieval failed: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlantManagementView(APIView):
    def post(self, request):
        """Plant a new plant"""
        try:
            garden = Garden.objects.filter(owner=request.user).first()
            serializer = PlantSerializer(data=request.data, context={"garden": garden})
            if serializer.is_valid(raise_exception=True):
                # Check if slot is empty
                if garden.plants.filter(
                    slot_position=serializer.validated_data["slot_position"]
                ).exists():
                    return Response(
                        {"status": "error", "error": "Slot already occupied"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                plant = serializer.save(
                    garden=garden,
                    plant_type=PlantType.objects.filter(
                        id=serializer.validated_data["plant_type_id"]
                    ).first(),
                )
                response_data = PlantSerializer(plant).data
                return Response(
                    {"status": "success", "data": {"plant_data": response_data}},
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "error": f"Plant management operation failed: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, plant_id):
        """Remove a plant"""
        try:
            garden = Garden.objects.filter(owner=request.user).first()
            plant = Plant.objects.filter(id=plant_id, garden=garden).first()
            plant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "error": f"Plant management operation failed: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
