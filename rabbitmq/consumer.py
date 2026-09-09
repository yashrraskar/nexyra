import os
import json
import logging
import httpx
from typing import Optional

from .connection import (
    get_pika_connection,
    register_fallback_subscriber,
    EXCHANGE_NAME,
    QUEUE_NAME,
    ROUTING_KEY
)

try:
    from goverment_systems.adapters.agriculture_adapter import convert_mahasync_to_agriculture
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent / "goverment_systems" / "adapters"))
    from agriculture_adapter import convert_mahasync_to_agriculture

logger = logging.getLogger("MahaSync.RabbitMQ.Consumer")
AGRICULTURE_API_URL = os.getenv("AGRICULTURE_API_URL", "http://127.0.0.1:8001")


async def handle_land_verified_message(event_data: dict) -> dict:
    """
    Processes LandVerified event:
    1. Transforms standardized MahaSync payload to Agriculture Department format via adapter.
    2. Transmits verification to Agriculture Department API.
    3. Confirms application status update.
    """
    logger.info(f"Consumer received event: {event_data.get('eventType')} for citizen: {event_data.get('citizenId')}")

    # Standardized MahaSync format expected by adapter:
    # citizenId, landId, landArea, verificationStatus
    mahasync_format = {
        "citizenId": event_data.get("citizenId"),
        "landId": event_data.get("landId"),
        "landArea": event_data.get("landArea", 0.0),
        "verificationStatus": event_data.get("verificationStatus", "VERIFIED")
    }

    # Step: Convert MahaSync format -> Agriculture Department format via Adapter
    agri_payload = convert_mahasync_to_agriculture(mahasync_format)
    logger.info(f"Standardized adapter output for Agriculture: {agri_payload}")

    # Step: Post verification to Agriculture Department endpoint
    url = f"{AGRICULTURE_API_URL}/agriculture/verify-land"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(url, json=agri_payload)
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Agriculture API successfully verified application: {result}")
                return {
                    "status": "success",
                    "agriculture_response": result,
                    "event": event_data
                }
            else:
                logger.error(f"Agriculture API returned error {response.status_code}: {response.text}")
                return {
                    "status": "failed",
                    "error": response.text,
                    "event": event_data
                }
        except Exception as e:
            logger.error(f"Failed to communicate with Agriculture API at {url}: {e}")
            return {
                "status": "network_error",
                "error": str(e),
                "event": event_data
            }


# Register fallback subscriber so in-process event bus automatically calls consumer
register_fallback_subscriber(ROUTING_KEY, handle_land_verified_message)


def start_pika_consumer_blocking():
    """Starts standalone blocking RabbitMQ consumer for production / Docker setups."""
    connection = get_pika_connection()
    if not connection:
        logger.error("Cannot start standalone pika consumer: RabbitMQ broker is unreachable.")
        return

    import pika
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)
    channel.basic_qos(prefetch_count=1)

    def on_message(ch, method, properties, body):
        import asyncio
        try:
            data = json.loads(body.decode("utf-8"))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(handle_land_verified_message(data))
            loop.close()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Error processing RabbitMQ message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    logger.info(f"RabbitMQ consumer listening on queue '{QUEUE_NAME}'...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()
