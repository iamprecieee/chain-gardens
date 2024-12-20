"""
Models for tracking blockchain metrics and weather conditions.
Provides real-time data for garden mechanics.
"""

from django.db.models import (
    Model,
    CharField,
    PositiveIntegerField,
    FloatField,
    DateTimeField,
)


class BlockchainMetrics(Model):
    timestamp = DateTimeField(auto_now_add=True, db_index=True)
    transaction_count = PositiveIntegerField()
    average_gas_price = PositiveIntegerField()
    block_number = PositiveIntegerField()
    network_load = FloatField()

    class Meta:
        ordering = ["-timestamp"]


class WeatherState(Model):
    """Current weather state calculated from blockchain metrics"""

    WEATHER_TYPES = [
        ("sunny", "Sunny"),
        ("cloudy", "Cloudy"),
        ("rainy", "Rainy"),
        ("stormy", "Stormy"),
    ]
    timestamp = DateTimeField(auto_now_add=True)
    weather_type = CharField(max_length=10, choices=WEATHER_TYPES, db_index=True)
    temperature = FloatField()  # Determined by network congestion
    rainfall = FloatField()  # Determined by transaction volume
    sunlight = FloatField()  # Determined by gas pricees

    class Meta:
        ordering = ["-timestamp"]
