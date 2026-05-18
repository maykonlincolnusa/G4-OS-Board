# API Gateway

Gateway central para autenticação, validação de tenant, roteamento e observabilidade de requests.

## Funcionalidades MVP
- Validação JWT básica.
- Enriquecimento de headers (`x-tenant-id`, `x-user-id`, `x-user-role`).
- Proxy para microsserviços.
- Catálogo de serviços.

## Run
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8080
```

