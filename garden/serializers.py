from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from .models import Garden, Plant, PlantType


class PlantTypeSerializer(ModelSerializer):
    class Meta:
        model = PlantType
        fields = [
            "id",
            "name",
            "growth_rate",
            "max_health",
            "required_soil_quality",
            "description",
        ]


class PlantSerializer(ModelSerializer):
    plant_type = PlantTypeSerializer(read_only=True)
    plant_type_id = CharField(write_only=True)

    class Meta:
        model = Plant
        fields = [
            "id",
            "plant_type",
            "plant_type_id",
            "growth_stage",
            "health",
            "growth_progress",
            "created",
            "updated",
            "slot_position",
            "growth_multiplier",
            "pest_damage",
        ]
        read_only_fields = [
            "id",
            "growth_stage",
            "health",
            "growth_progress",
            "created",
            "updated",
            "growth_multiplier",
            "pest_damage",
        ]

    def validate_slot_position(self, value):
        garden = self.context["garden"]
        if value >= garden.plot_size:
            raise ValidationError(
                f"Invalid slot position. Garden only has {garden.plot_size} slots."
            )
        return value


class GardenSerializer(ModelSerializer):
    plants = PlantSerializer(many=True, read_only=True)

    class Meta:
        model = Garden
        fields = [
            "id",
            "level",
            "soil_quality",
            "plot_size",
            "plants",
            "created",
            "updated",
            "pest_infestation",
            "pest_type",
            "pest_severity",
            "last_activity",
            "total_onchain_actions",
        ]
        read_only_fields = [
            "id",
            "level",
            "soil_quality",
            "plot_size",
            "created",
            "updated",
            "pest_infestation",
            "pest_type",
            "pest_severity",
            "last_activity",
            "total_onchain_actions",
        ]
