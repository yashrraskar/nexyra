import os
import json
import logging
import asyncio
from typing import Callable, Dict, List

logger = logging.getLogger("MahaSync.RabbitMQ")

AMQP_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE_NAME = "mahasync.events"
EXCHANGE_TYPE = "topic"
QUEUE_NAME = "agriculture.land_verified"
ROUTING_KEY = "land.verified"

# In-memory async fallback subscribers for local zero-dependency execution
_fallback_subscribers: Dict[str, List[Callable]] = {}


def register_fallback_subscriber(routing_key: str, callback: Callable):
    """Registers a handler for in-process asynchronous dispatch when RabbitMQ broker is offline."""
    if routing_key not in _fallback_subscribers:
        _fallback_subscribers[routing_key] = []
    _fallback_subscribers[routing_key].append(callback)


async def dispatch_fallback_event(routing_key: str, payload: dict):
    """Dispatches event to in-process subscribers asynchronously."""
    matched_handlers = []
    for pattern, handlers in _fallback_subscribers.items():
        if pattern == routing_key or pattern == "#" or (pattern.endswith(".*") and routing_key.startswith(pattern[:-2])):
            matched_handlers.extend(handlers)

    for handler in matched_handlers:
        try:
            if asyncio.iscoroutinefunction(handler):
                asyncio.create_task(handler(payload))
            else:
                handler(payload)
        except Exception as e:
            logger.error(f"Error in fallback subscriber for {routing_key}: {e}")


def get_pika_connection():
    """Attempts to establish connection with real RabbitMQ broker via pika."""
    try:
        import pika
        parameters = pika.URLParameters(AMQP_URL)
        parameters.socket_timeout = 2.0
        connection = pika.BlockingConnection(parameters)
        return connection
    except Exception as e:
        logger.warning(f"Could not connect to RabbitMQ broker at {AMQP_URL}: {e}. Using simulated event bus fallback.")
        return None
