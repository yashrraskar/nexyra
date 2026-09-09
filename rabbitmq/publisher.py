import json
import logging
from .connection import (
    get_pika_connection,
    dispatch_fallback_event,
    EXCHANGE_NAME,
    EXCHANGE_TYPE,
    ROUTING_KEY
)

logger = logging.getLogger("MahaSync.RabbitMQ.Publisher")


async def publish_event(event_data: dict, routing_key: str = ROUTING_KEY) -> dict:
    """
    Publishes an event to the RabbitMQ exchange.
    Falls back gracefully to asynchronous in-process event bus if broker is offline.
    """
    payload_str = json.dumps(event_data, default=str)
    connection = get_pika_connection()

    if connection:
        try:
            import pika
            channel = connection.channel()
            # Declare durable exchange
            channel.exchange_declare(
                exchange=EXCHANGE_NAME,
                exchange_type=EXCHANGE_TYPE,
                durable=True
            )
            # Publish persistent message
            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key=routing_key,
                body=payload_str.encode("utf-8"),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type="application/json",
                    app_id="mahasync-backend"
                )
            )
            connection.close()
            logger.info(f"Published event '{event_data.get('eventType')}' to RabbitMQ exchange '{EXCHANGE_NAME}' [{routing_key}]")
            return {
                "status": "published",
                "transport": "rabbitmq",
                "exchange": EXCHANGE_NAME,
                "routing_key": routing_key
            }
        except Exception as e:
            logger.error(f"Failed to publish via pika: {e}. Falling back to in-process event dispatch.")

    # Fallback to in-process asynchronous dispatch
    await dispatch_fallback_event(routing_key, event_data)
    logger.info(f"Published event '{event_data.get('eventType')}' to in-process event bus [{routing_key}]")
    return {
        "status": "published",
        "transport": "in_process_event_bus",
        "exchange": EXCHANGE_NAME,
        "routing_key": routing_key
    }
