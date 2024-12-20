from celery import shared_task
from .services import BlockchainMonitor
from user.models import User
from garden.services import GrowthService


@shared_task(max_retries=5)
def update_blockchain_metrics():
    """Update blockchain metrics and weather state."""
    monitor = BlockchainMonitor()
    try:
        metrics = monitor.get_current_metrics()
        if metrics:
            return {
                "status": "success",
                "block_number": metrics.block_number,
                "transaction_count": metrics.transaction_count,
                "network_load": metrics.network_load,
            }
        return {"status": "error", "message": "No metrics collected"}
    except Exception as e:
        print(f"Failed to update blockchain metrics: {str(e)}")
        return {"status": "error", "message": str(e)}


@shared_task(max_retries=5)
def monitor_user_activities():
    """Monitor blockchain activities for all users"""
    try:
        monitor = BlockchainMonitor()
        activity_count = 0
        for user in User.objects.filter(is_active=True, garden__isnull=False):
            if user.wallet_address:
                print(f"Checking activities for wallet: {user.wallet_address}")
                activities = monitor.monitor_user_activity(user.wallet_address)
                # Process activities for user's garden
                for activity in activities:
                    print(f"Processing {activity} for {user.wallet_address}")
                    GrowthService.process_user_activity(user.garden, activity)
                    activity_count += 1
                # Check for pest infestations
                GrowthService.check_for_pests(user.garden)
        return {
            "status": "success",
            "message": f"Processed {activity_count} user activities",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
