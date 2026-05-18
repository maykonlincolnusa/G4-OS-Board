from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("/tmp/boardpacks")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_markdown(title: str, payload: dict) -> Path:
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    target = OUTPUT_DIR / f"boardpack_{ts}.md"
    content = f"""# {title}

## 1. Capa
Board Governance OS AI

## 2. Resumo executivo
{payload.get('executive_summary', 'Resumo indisponível.')}

## 3. Principais KPIs
- Receita mensal
- Churn
- CAC
- LTV

## 4. Receita e crescimento
## 5. Marketing e vendas
## 6. Produto e tecnologia
## 7. Comunidade/clientes/alunos
## 8. Operações
## 9. Financeiro
## 10. Riscos
## 11. Decisões pendentes
## 12. Ações atrasadas
## 13. Perguntas recomendadas para o board
## 14. Recomendações dos agentes
## 15. Apêndice com fontes
"""
    target.write_text(content, encoding="utf-8")
    return target

