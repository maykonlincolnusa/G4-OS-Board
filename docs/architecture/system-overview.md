# System Overview

Board Governance OS AI é um sistema operacional de governança executiva orientado a microsserviços, eventos e agentes de IA.

Camadas:
1. Experience Layer: `apps/web`, `apps/admin`.
2. Control Plane: `apps/api-gateway`, auth, tenant, admin-ops.
3. Governance Core: board, meetings, decisions, actions, risk, approvals, audit.
4. Intelligence Plane: document-intelligence, rag, agent-orchestrator, agent-registry, skills-playbook.
5. Integration Plane: channel-governance, integration, notification.
6. Data Plane: PostgreSQL + pgvector, Redis, object storage.

