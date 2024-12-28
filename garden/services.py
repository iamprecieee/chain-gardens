"""
Core business logic for garden mechanics.
Handles growth calculations, pest management, and blockchain activity integration.
"""

from django.utils import timezone
from datetime import timedelta
from blockchain.models import WeatherState
import random


class GrowthService:
    PEST_TYPES = {
        "aphids": {"damage": 0.2, "solution": "transfer"},
        "slugs": {"damage": 0.3, "solution": "transfer"}, # Temporary solution
        "fungus": {"damage": 0.4, "solution": "transfer"},
    }
    BASE_GROWTH_RATE = 0.05

    @staticmethod
    def calculate_growth(plant, weather):
        """Calculate plant growth based on conditions"""
        try:
            base_growth = plant.plant_type.growth_rate * GrowthService.BASE_GROWTH_RATE
            # Weather effects
            weather_multipliers = {
                "sunny": 0.5,
                "cloudy": 0.3,
                "rainy": 0.2,
                "stormy": 0.1,
            }
            # Calculate growth
            weather_effect = weather_multipliers.get(weather.weather_type, 1.0)
            soil_effect = plant.garden.soil_quality / 100
            health_effect = plant.health / 100
            # Apply pest damage reduction
            pest_reduction = 1.0
            if plant.garden.pest_infestation:
                pest_reduction = max(0.1, 1 - (plant.pest_damage / 100))
            growth_amount = (
                base_growth
                * weather_effect
                * soil_effect
                * health_effect
                * pest_reduction
            )
            return growth_amount
        except Exception as e:
            raise Exception(f"Failed to calculate growth: {str(e)}")

    @staticmethod
    def check_for_pests(garden):
        """Random pest infestations based on conditions"""
        try:
            if garden.pest_infestation:
                return
            # Higher chance during certain weather conditions
            base_chance = 0.05  # 5% base chance
            if (
                not garden.last_activity
                or (timezone.now() - garden.last_activity).days > 2
            ):
                base_chance *= 2  # Double chance if inactive
            if random.random() < base_chance:
                pest_type = random.choice(list(GrowthService.PEST_TYPES.keys()))
                garden.pest_infestation = True
                garden.pest_type = pest_type
                garden.pest_severity = random.randint(30, 70)
                garden.save()
                # Apply initial damage to plants
                for plant in garden.plants.all():
                    plant.pest_damage = garden.pest_severity
                    plant.save()
        except Exception as e:
            raise Exception(f"Failed to check for pests: {str(e)}")

    @staticmethod
    def process_user_activity(garden, activity_type):
        """Process blockchain activity effects"""
        try:
            activities = {
                "transfer": {"growth": 0.2, "pest_resistance": 0.3},
                # "swap": {"growth": 0.3, "pest_resistance": 0.2},
                # "stake": {"growth": 0.4, "pest_resistance": 0.4},
            }
            if activity_type in activities:
                # Update activity timestamp
                garden.last_activity = timezone.now()
                garden.total_onchain_actions += 1
                # Check if this activity solves pest problem
                if (
                    garden.pest_infestation
                    and activity_type
                    == GrowthService.PEST_TYPES[garden.pest_type]["solution"]
                ):
                    garden.pest_infestation = False
                    garden.pest_type = None
                    garden.pest_severity = 0
                    # Heal plants
                    for plant in garden.plants.all():
                        plant.pest_damage = 0
                        plant.save()
                # Apply growth boost to plants
                boost = activities[activity_type]["growth"]
                for plant in garden.plants.all():
                    plant.growth_multiplier = min(2.0, plant.growth_multiplier + boost)
                    plant.save()
                garden.save()
        except Exception as e:
            raise Exception(f"Failed to process user activity: {str(e)}")

    @staticmethod
    def update_plant_stage(plant):
        """Update plant growth stage based on progress"""
        try:
            if plant.growth_progress >= 100:
                plant.growth_stage = "harvest"
            elif plant.growth_progress >= 80:
                plant.growth_stage = "flowering"
            elif plant.growth_progress >= 60:
                plant.growth_stage = "mature"
            elif plant.growth_progress >= 30:
                plant.growth_stage = "growing"
            elif plant.growth_progress >= 10:
                plant.growth_stage = "sprout"
        except Exception as e:
            raise Exception(f"Failed to update plant stage: {str(e)}")

    @staticmethod
    def update_plant_health(plant, weather):
        """Update plant health based on conditions"""
        try:
            # Base health change
            health_change = 0
            # Weather effects
            if weather.weather_type == "stormy":
                health_change -= 5
            elif weather.weather_type == "sunny" and weather.temperature > 35:
                health_change -= 2
            elif weather.weather_type == "rainy" and plant.growth_stage in [
                "flowering",
                "harvest",
            ]:
                health_change -= 3
            # Soil quality effects
            if plant.garden.soil_quality < plant.plant_type.required_soil_quality:
                health_change -= 2
            # Apply health change
            plant.health = max(0, min(100, plant.health + health_change))
            return health_change
        except Exception as e:
            raise Exception(f"Failed to update plant health: {str(e)}")

    @classmethod
    def process_growth_cycle(cls):
        """Process growth for all plants"""
        try:
            from .models import Plant

            current_weather = WeatherState.objects.filter(
                timestamp__gte=timezone.now() - timedelta(minutes=30)
            ).first()
            if not current_weather:
                return
            for plant in Plant.objects.select_related("garden", "plant_type"):
                if plant.growth_stage != "harvest":
                    # Calculate and apply growth
                    growth = cls.calculate_growth(plant, current_weather)
                    plant.growth_progress = min(100, plant.growth_progress + growth)
                    # Update health
                    cls.update_plant_health(plant, current_weather)
                    # Update stage
                    cls.update_plant_stage(plant)
                    plant.last_updated = timezone.now()
                    plant.save()
        except Exception as e:
            raise Exception(f"Failed to process growth cycle: {str(e)}")
