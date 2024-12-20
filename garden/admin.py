from django.contrib.admin import register, ModelAdmin
from .models import Garden, PlantType, Plant


@register(Garden)
class GardenAdmin(ModelAdmin):
    list_display = [
        "id",
        "level",
        "soil_quality",
        "plot_size",
        "owner",
        "created",
        "updated",
    ]
    list_filter = ["id", "level", "owner", "plot_size", "created"]
    readonly_fields = ["id", "created", "owner"]


@register(PlantType)
class PlantTypeAdmin(ModelAdmin):
    list_display = [
        "id",
        "name",
        "growth_rate",
        "max_health",
        "required_soil_quality",
        "created",
    ]
    list_filter = [
        "name", 
        "growth_rate", 
        "max_health", 
        "required_soil_quality", 
        "created"
    ]
    readonly_fields = ["id", "created"]
    search_fields = ["name", "description"]


@register(Plant)
class PlantAdmin(ModelAdmin):
    list_display = [
        "id",
        "garden",
        "plant_type",
        "growth_stage",
        "health",
        "growth_progress",
        "slot_position",
        "created",
        "updated",
    ]
    list_filter = [
        "garden",
        "plant_type",
        "growth_stage",
        "health",
        "created",
    ]
    readonly_fields = ["id", "created"]
    search_fields = ["plant_type__name", "garden__id"]