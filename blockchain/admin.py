from django.contrib.admin import register, ModelAdmin
from .models import BlockchainMetrics, WeatherState


@register(BlockchainMetrics)
class BlockchainMetricsAdmin(ModelAdmin):
    list_display = [
        "timestamp",
        "transaction_count",
        "average_gas_price",
        "block_number",
        "network_load",
    ]
    list_filter = [
        "timestamp",
        "transaction_count",
        "average_gas_price",
        "block_number",
    ]
    readonly_fields = ["timestamp"]


@register(WeatherState)
class WeatherStateAdmin(ModelAdmin):
    list_display = [
        "timestamp",
        "weather_type",
        "temperature",
        "rainfall",
        "sunlight",
    ]
    list_filter = [
        "timestamp",
        "weather_type",
        "temperature",
        "rainfall",
        "sunlight",
    ]
    readonly_fields = ["timestamp"]