# RabbitMQ Interoperability Event Bus (Member 4)

## Architecture Overview
MahaSync uses RabbitMQ to implement asynchronous, event-driven integration between independent government departments. By decoupling systems through an event bus:
1. The **Revenue Department** is not directly coupled to the **Agriculture Department**.
2. Departmental systems can process events at their own pace without cascading HTTP timeouts.
3. Message durability and delivery guarantees are preserved.

## Event Flow Topology
```text
[MahaSync Backend]
       │
       ▼ (Publishes LandVerifiedEvent)
[Exchange: mahasync.events] (Type: topic, Durable: true)
       │
       ├── Binding Key: "land.verified"
       ▼
[Queue: agriculture.land_verified] (Durable: true, Prefetch: 1)
       │
       ▼ (Consumes message)
[RabbitMQ Consumer Worker]
       │
       ├── Invokes agriculture_adapter.py
       ▼
[Agriculture Department API: POST /agriculture/verify-land]
```

## Event Contract: `LandVerified`
```json
{
  "eventType": "LandVerified",
  "citizenId": "C001",
  "landId": "MH-LAND-101",
  "landArea": 2.5,
  "verificationStatus": "VERIFIED",
  "source": "Revenue",
  "applicationId": "APP-2026-001",
  "timestamp": "2026-09-10T00:00:00.000Z"
}
```

## Key Files
- `connection.py`: Broker connection manager with automatic in-process asynchronous fallback for zero-dependency local demonstration.
- `publisher.py`: Declares durable exchange and persistent messages (`delivery_mode=2`).
- `consumer.py`: Consumer worker converting standardized payloads and invoking the Agriculture endpoint.
- `schemas.py`: Pydantic event contracts.
- `definitions.json`: Declarative topology for Docker initialization.

## Running Standalone
To run a standalone RabbitMQ container with pre-configured definitions:
```bash
docker run -d --name mahasync-rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  -v $(pwd)/definitions.json:/etc/rabbitmq/definitions.json:ro \
  -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbitmq_management load_definitions \"/etc/rabbitmq/definitions.json\"" \
  rabbitmq:3.13-management
```
Management UI will be available at `http://localhost:15672` (User: `guest`, Password: `guest`).
