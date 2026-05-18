# channel-governance-service

## Purpose
Microservice responsible for channel-governance-service domain capabilities in the Board Governance OS AI platform.

## Layers
- pp/api: FastAPI routes and contracts.
- pp/core: Config, telemetry and cross-cutting concerns.
- pp/domain: Domain entities and business rules.
- pp/schemas: Request/response schemas.
- pp/services: Application services and use-cases.
- pp/repositories: Persistence adapters.
- pp/tests: Unit and integration tests.

## Run
`ash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
`

## Environment Variables
See .env.example.

## Example Payload
`json
{ "tenant_id": "tenant-demo", "request_id": "req-123" }
`

## Integrations
This service consumes tenant context headers from API Gateway and publishes domain events to Redis Streams/Kafka.

