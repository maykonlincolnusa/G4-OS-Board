# Board Governance OS AI

Protótipo enterprise de um sistema operacional de governança executiva com IA, inspirado em necessidades reais de ecossistemas de educação executiva, operações de diretoria e conselho.

> Aviso de marca: este projeto é conceitual, sem afiliação oficial ao G4 ou a qualquer marca de terceiros, salvo autorização formal futura.

## 1. Problema
Decisões críticas ficam espalhadas entre reuniões, WhatsApp, e-mails, planilhas, documentos e CRMs, sem trilha auditável nem execução disciplinada.

## 2. Solução
Uma plataforma SaaS B2B multi-tenant que centraliza governança, memória de decisão, execução operacional, riscos e inteligência de IA com RAG e agentes especializados.

## 3. Arquitetura
- Monorepo modular por domínio (`apps`, `services`, `agents`, `packages`, `database`, `infra`, `docs`, `tests`).
- Microsserviços em FastAPI (Python 3.12+).
- Frontend Next.js 15 + TypeScript + Tailwind.
- PostgreSQL + pgvector, Redis e event backbone.
- LangGraph para orquestração de agentes.

## 4. Estrutura do Repositório
```text
/apps
  /web
  /admin
  /api-gateway
/services
  /auth-service
  /tenant-service
  /user-service
  /board-service
  /meeting-service
  /decision-memory-service
  /action-tracker-service
  /document-intelligence-service
  /rag-service
  /agent-orchestrator-service
  /agent-registry-service
  /skills-playbook-service
  /risk-compliance-service
  /approval-workflow-service
  /channel-governance-service
  /notification-service
  /analytics-kpi-service
  /audit-ledger-service
  /board-pack-generator-service
  /integration-service
  /billing-service
  /admin-ops-service
/agents
/packages
/database
/infra
/docs
/tests
```

## 5. Microsserviços
Cada serviço contém:
- `app/api`, `app/core`, `app/domain`, `app/schemas`, `app/services`, `app/repositories`, `app/tests`
- `Dockerfile`, `README.md`, `.env.example`, `requirements.txt`

## 6. Agentes
Agentes iniciais incluídos:
- Executive Board Agent
- Board Secretary Agent
- Decision Intelligence Agent
- Risk Officer Agent
- CFO Analyst Agent
- Revenue & Growth Agent
- Customer Success Agent
- Operations Agent
- Legal & Compliance Agent
- Product & Content Agent
- Community Intelligence Agent
- Channel Monitor Agent
- Playbook Builder Agent
- Governance Coach Agent
- AI Quality Evaluator Agent

## 7. Stack
- Frontend: Next.js 15, React, TypeScript, Tailwind
- Backend: FastAPI, Python 3.12+
- Banco: PostgreSQL + pgvector
- Cache/Eventos MVP: Redis
- IA: OpenAI API (com fallback), LangGraph
- Observabilidade: logs JSON, OpenTelemetry-ready, LangSmith-ready
- Deploy local: Docker Compose

## 8. Rodar Local
1. Criar `.env` na raiz com base em `.env.example`.
2. Subir infraestrutura:
```bash
docker compose -f infra/docker/docker-compose.yml up --build
```
3. Aplicar migrations/seeds (se necessário manualmente):
```bash
psql -h localhost -U board_user -d board_os -f database/migrations/001_init.sql
psql -h localhost -U board_user -d board_os -f database/seeds/001_seed.sql
```
4. Abrir apps:
- Web: `http://localhost:3000`
- API Gateway: `http://localhost:8080`

## 9. Variáveis de Ambiente
Ver `.env.example` e os `.env.example` de cada serviço.

## 10. Migrations e Seeds
- Migration inicial: `database/migrations/001_init.sql`
- Seeds fictícios: `database/seeds/001_seed.sql`

## 11. Testes
Exemplos (por serviço):
```bash
pytest services/auth-service/app/tests
pytest services/decision-memory-service/app/tests
pytest services/rag-service/app/tests
pytest services/agent-orchestrator-service/app/tests
pytest services/action-tracker-service/app/tests
```

## 12. MVP Entregue nesta Base
- Auth JWT básico
- Tenant isolation por header
- Upload/ingestão de documentos
- RAG inicial com citações
- Board AI chat (via orchestrator)
- Meetings + sumarização base
- Decision memory
- Action tracker
- Risk center
- Board pack generator (Markdown + contratos para PDF/PPTX/DOCX/XLSX)
- Dashboard executivo inicial
- Audit logs básicos
- Seeds de cenário corporativo

## 13. Segurança
- Validação `x-tenant-id` em endpoints críticos
- RBAC modelado
- Separação de nível de acesso (`public`, `internal`, `confidential`, `board_only`)
- Detecção básica de prompt injection em ingestão
- Trilha de auditoria por serviço

## 14. Governança
- Memória de decisão estruturada
- Ações rastreáveis com responsável e prazo
- Riscos com probabilidade x impacto
- Aprovação e compliance prontos para evolução

## 15. Observabilidade
- Logs estruturados JSON (boilerplate)
- Campos de correlação definidos em `packages/observability/logging.md`
- Base pronta para integração com OpenTelemetry, Sentry e LangSmith

## 16. Screenshots
Placeholders:
- `docs/screenshots/dashboard.png`
- `docs/screenshots/board-chat.png`
- `docs/screenshots/board-pack.png`

## 17. Roadmap
1. Persistência completa por serviço (SQLAlchemy + migrations por domínio).
2. Conectores reais (Gmail, Calendar, Slack, Teams, CRM).
3. Pipeline completo de documentos e geração nativa PDF/PPTX/DOCX/XLSX.
4. LangSmith tracing fim-a-fim e avaliação contínua de agentes.
5. White-label e billing enterprise.

## 18. How this project can be adapted

### 18.1 Uso interno em empresa
- Manter: `auth`, `tenant`, `meeting`, `decision-memory`, `action-tracker`, `risk`, `audit`, `analytics`.
- Opcional remover: `billing-service`, `skills-playbook-service`, `channel-governance-service`.

### 18.2 Escola de negócios
- Reforçar: `community`, `courses`, `events` via `analytics`, `channel-governance`, `document-intelligence`.
- Adicionar templates específicos de programas, turmas e mentorias.

### 18.3 Consultorias
- Manter isolamento por cliente (tenant) e playbooks reutilizáveis.
- Usar `skills-playbook-service` + `agent-registry` como diferencial de delivery.

### 18.4 SaaS white-label
- Separar branding por tenant em `apps/web`.
- Expandir `billing-service`, `admin-ops-service`, `integration-service`.

### 18.5 Plataforma de board e diretoria
- Priorizar `meeting`, `decision-memory`, `board-pack-generator`, `risk`, `audit`.
- Evoluir controle de comitês e cadências por board.

### 18.6 Exemplos por contexto
- Educação executiva: foco em cursos, mentorias, comunidade e eventos.
- Consultorias: foco em replicabilidade de playbooks.
- Empresas familiares: foco em governança, sucessão e compliance.
- Startups: foco em crescimento, runway e execução quinzenal.
- Holdings: foco em visão multi-unidade e consolidação de risco.
- Conselhos administrativos: foco em ata, decisões e accountability.
- Operações comerciais: foco em funil, conversão e previsibilidade.
- Customer Success: foco em health score e churn prevention.
- IA corporativa: foco em RAG seguro e governado.

## 19. Módulos para versão menor vs enterprise
- Versão menor: `auth`, `tenant`, `meeting`, `decision-memory`, `action-tracker`, `rag`, `agent-orchestrator`, `web`.
- Versão enterprise (recomendada): todos os serviços + `audit`, `risk`, `approval`, `channels`, `integrations`, `billing`, `admin-ops`.

## 20. Licença
MIT.

