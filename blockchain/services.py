from web3 import Web3
from django.conf import settings
from .models import BlockchainMetrics, WeatherState
from django.utils import timezone
import requests


class BlockchainMonitor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ABSTRACT["RPC_URL"]))
        self.last_processed_block = None
        self.explorer_api_url = settings.ABSTRACT["EXPLORER_API_URL"]

    def check_connection(self):
        """Verifies connection to the blockchain."""
        try:
            is_connected = self.w3.is_connected()
            current_block = (
                self.w3.eth.get_block("latest", True) if is_connected else None
            )
            gas_price = self.w3.eth.gas_price if is_connected else None
            return {
                "connected": True,
                "current_block": current_block,
                "gas_price": gas_price,
            }
        except Exception as e:
            return {"connected": False, "error": str(e)}

    def get_current_metrics(self):
        """Collects current blockchain metrics."""
        try:
            connection_status = self.check_connection()
            if not connection_status["connected"]:
                return None
            current_block = connection_status["current_block"]
            gas_price = connection_status["gas_price"]
            metrics, created = BlockchainMetrics.objects.get_or_create(
                defaults={
                    "transaction_count": len(current_block["transactions"]),
                    "average_gas_price": gas_price,
                    "block_number": current_block["number"],
                    "network_load": min(len(current_block["transactions"]) / 100, 1.0),
                }
            )
            if not created:
                # Update existing record
                metrics.transaction_count = len(current_block["transactions"])
                metrics.average_gas_price = gas_price
                metrics.block_number = current_block["number"]
                metrics.network_load = min(
                    len(current_block["transactions"]) / 100, 1.0
                )
                metrics.timestamp = timezone.now()
                metrics.save()
            self._update_weather(metrics)
            return metrics
        except Exception as e:
            raise Exception(f"Failed to retrieve metrics: {str(e)}")

    def _update_weather(self, metrics):
        """Updates weather based on blockchain metrics."""
        try:
            # Determine weather type based on network load
            if metrics.network_load > 0.8:
                weather_type = "stormy"
                # Stormy weather is cooler
                temperature = 15 + (metrics.network_load * 10)
            elif metrics.network_load > 0.5:
                weather_type = "rainy"
                # Rain brings moderate temperatures
                temperature = 18 + (metrics.network_load * 12)
            elif metrics.network_load > 0.3:
                weather_type = "cloudy"
                # Cloudy conditions have mild temperatures
                temperature = 20 + (metrics.network_load * 15)
            else:
                weather_type = "sunny"
                # Sunny weather can be quite warm
                temperature = 25 + (metrics.network_load * 20)
            weather, created = WeatherState.objects.get_or_create(
                defaults={
                    "weather_type": weather_type,
                    "temperature": temperature,  # 20-40 degrees
                    "rainfall": metrics.transaction_count / 100,
                    "sunlight": 100 - (metrics.network_load * 100),
                }
            )
            if not created:
                # Update existing record
                weather.weather_type = weather_type
                weather.temperature = 20 + (metrics.network_load * 20)
                weather.rainfall = metrics.transaction_count / 100
                weather.sunlight = 100 - (metrics.network_load * 100)
                weather.timestamp = timezone.now()
                weather.save()
        except Exception as e:
            raise Exception(f"Failed to update weather: {str(e)}")

    def monitor_user_activity(self, user_address):
        """Monitor specific user's blockchain activity"""
        try:
            # Get user's garden and last processed transaction
            from garden.models import Garden
            garden = Garden.objects.filter(owner__wallet_address=user_address).first()
            if not garden:
                return []
            params = {
                "module": "account",
                "action": "txlist",
                "page": 1,
                "offset": 10,
                "sort": "desc",
                "address": user_address,
                "startblock": 0,
                "endblock": 99999999,
            }
            response = requests.get(self.explorer_api_url, params=params, timeout=50)
            if not response.ok:
                return []
            data = response.json()
            if data.get("status") != "1":
                return []
            transactions = data.get("result", [])
            activities = []
            # Get current block timestamp
            current_block = self.w3.eth.get_block("latest")
            current_timestamp = current_block["timestamp"]
            cutoff_time = current_timestamp - (5 * 60)  # 5 minutes ago
            newest_hash = None
            for tx in transactions:
                if newest_hash is None:
                    newest_hash = tx['hash']
                if garden.last_processed_hash and tx['hash'] <= garden.last_processed_hash:
                    break
                try:
                    timestamp = int(tx["timeStamp"])
                    if timestamp < cutoff_time:
                        continue
                    if tx.get("isError") == "1":
                        continue
                    # Check value and method ID
                    if int(tx.get("value", "0")) > 0:
                        activities.append("transfer")
                    method_id = tx.get("methodId", "").lower()
                    if method_id == "0x38ed1739":  # swap
                        activities.append("swap")
                    elif method_id == "0xa694fc3a":  # stake
                        activities.append("stake")
                except Exception as tx_error:
                    continue
            # Update the last processed hash to the newest transaction we've seen
            if newest_hash and newest_hash != garden.last_processed_hash:
                garden.last_processed_hash = newest_hash
                garden.save()
            return activities
        except requests.Timeout:
            raise
        except Exception as e:
            raise Exception(f"Failed to monitor user activity: {str(e)}")
