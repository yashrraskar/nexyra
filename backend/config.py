import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Database configuration: defaults to local SQLite for zero-friction demo, supports PostgreSQL via env
DEFAULT_DB_PATH = BASE_DIR / "mahasync.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# Department APIs
REVENUE_API_URL = os.getenv("REVENUE_API_URL", "http://127.0.0.1:8000")
AGRICULTURE_API_URL = os.getenv("AGRICULTURE_API_URL", "http://127.0.0.1:8001")

# RabbitMQ & Keycloak
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "mahasync")
ENABLE_KEYCLOAK = os.getenv("ENABLE_KEYCLOAK", "false").lower() == "true"

# Server Host and Port
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8082"))
