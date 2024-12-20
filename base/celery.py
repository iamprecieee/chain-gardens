"""
Celery configuration for Chain Gardens.
Handles periodic tasks for blockchain monitoring and garden updates.
"""

import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
app = Celery("chain_gardens")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Scheduled Tasks
app.conf.beat_schedule = {
    "update-blockchain-metrics": {
        "task": "blockchain.tasks.update_blockchain_metrics",
        "schedule": 300.0, # Increased to 5 minutes
    },
    "process_garden_updates": {
        "task": "garden.tasks.process_garden_updates",
        "schedule": 300.0,
    },
    "monitor_user_activities": {
        "task": "blockchain.tasks.monitor_user_activities",
        "schedule": 300.0,
    },
}
