from rest_framework.serializers import ModelSerializer
from .models import WeatherState


class WeatherStateSerializer(ModelSerializer):
    class Meta:
        model = WeatherState
        fields = ["weather_type", "temperature", "rainfall", "sunlight", "timestamp"]
