"""
Core models for the garden system.
Handles garden plots, plants, and growth mechanics.
"""

from django.db.models import (
    Model,
    CharField,
    PositiveIntegerField,
    FloatField,
    TextField,
    DateTimeField,
    OneToOneField,
    ForeignKey,
    CASCADE,
    UniqueConstraint,
    PROTECT,
    BooleanField,
)
from django.contrib.auth import get_user_model
from base.utils import generate_id


User = get_user_model()


class Garden(Model):
    id = CharField(
        max_length=21,
        primary_key=True,
        editable=False,
        unique=True,
        default=generate_id,
    )
    owner = OneToOneField(User, on_delete=CASCADE, related_name="garden", db_index=True)
    level = PositiveIntegerField(default=1)
    soil_quality = PositiveIntegerField(default=100)  # 0-100
    plot_size = PositiveIntegerField(default=4)  # Number of plant slots
    pest_infestation = BooleanField(default=False)
    pest_type = CharField(max_length=20, null=True)
    pest_severity = PositiveIntegerField(default=0)  # 0-100
    last_activity = DateTimeField(null=True)  # Track user's last onchain activity
    total_onchain_actions = PositiveIntegerField(default=0)
    last_processed_hash = CharField(
        max_length=66, null=True, db_index=True
    )  # Transaction hash is 66 chars with '0x'
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]


class PlantType(Model):
    """Different types of plants available"""

    id = CharField(max_length=21, primary_key=True, editable=False, default=generate_id)
    name = CharField(max_length=100)
    growth_rate = FloatField()  # Base growth rate
    max_health = PositiveIntegerField()
    required_soil_quality = PositiveIntegerField()
    description = TextField()
    created = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name


class Plant(Model):
    """Individual plant instance in a garden"""

    STAGE_CHOICES = [
        ("seed", "Seed"),
        ("sprout", "Sprout"),
        ("growing", "Growing"),
        ("mature", "Mature"),
        ("flowering", "Flowering"),
        ("harvest", "Ready to Harvest"),
    ]
    id = CharField(max_length=21, primary_key=True, editable=False, default=generate_id)
    garden = ForeignKey(Garden, on_delete=CASCADE, related_name="plants")
    plant_type = ForeignKey(PlantType, on_delete=PROTECT)
    growth_stage = CharField(max_length=10, choices=STAGE_CHOICES, default="seed")
    health = PositiveIntegerField(default=100)  # 0-100
    growth_progress = FloatField(default=0)  # 0-100
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    slot_position = PositiveIntegerField()  # Position in garden (0 to plot_size-1)
    pest_damage = PositiveIntegerField(default=0)  # 0-100
    growth_multiplier = FloatField(default=1.0)  # Affected by user activity

    class Meta:
        ordering = ["-created"]
        constraints = [
            UniqueConstraint(
                fields=["garden", "slot_position"], name="unique_garden_slot"
            )
        ]

    def __str__(self):
        return self.plant_type.name
