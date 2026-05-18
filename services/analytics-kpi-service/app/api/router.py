from fastapi import APIRouter, Header, HTTPException

router = APIRouter(prefix="/api/v1", tags=["analytics"])

KPI_SNAPSHOT = [
    {"metric": "Receita Mensal", "value": 2950000, "trend": "+12%", "status": "good"},
    {"metric": "Leads", "value": 18200, "trend": "+9%", "status": "good"},
    {"metric": "Churn", "value": 2.1, "trend": "-0.3pp", "status": "good"},
    {"metric": "Ações Atrasadas", "value": 14, "trend": "+2", "status": "warning"},
    {"metric": "Riscos Abertos", "value": 23, "trend": "+1", "status": "warning"},
]


@router.get("/dashboard/executive")
def executive_dashboard(x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")
    return {
        "tenant_id": x_tenant_id,
        "kpis": KPI_SNAPSHOT,
        "highlights": [
            "Receita acima da meta mensal.",
            "Risco financeiro de inadimplência requer mitigação.",
            "Backlog de ações estratégicas precisa aceleração.",
        ],
    }

