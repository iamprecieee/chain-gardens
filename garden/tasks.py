from celery import shared_task
from django.utils import timezone
from .services import GrowthService


@shared_task(max_retries=5)
def process_garden_updates():
    """Process growth updates for all plants."""
    try:
        start_time = timezone.now()
        plants_updated = GrowthService.process_growth_cycle()
        end_time = timezone.now()
        return {
            "status": "success",
            "plants_updated": plants_updated,
            "duration": (end_time - start_time).total_seconds(),
        }
    except Exception as e:
        raise Exception(f"Failed to process garden updates: {str(e)}")
