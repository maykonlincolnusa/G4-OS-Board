import { KpiCard } from "@/components/kpi-card";

export default function DashboardPage() {
  return (
    <section className="space-y-6">
      <div className="panel p-5">
        <h2 className="text-xl font-semibold">Executive Dashboard</h2>
        <p className="mt-1 text-sm text-muted">Visão consolidada de performance, execução e riscos.</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <KpiCard title="Receita Mensal" value="R$ 2,95M" trend="+12%" status="good" />
        <KpiCard title="Leads" value="18.200" trend="+9%" status="good" />
        <KpiCard title="Churn" value="2,1%" trend="-0,3pp" status="good" />
        <KpiCard title="Ações Atrasadas" value="14" trend="+2" status="warning" />
        <KpiCard title="Riscos Abertos" value="23" trend="+1" status="risk" />
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <article className="panel p-5">
          <h3 className="font-semibold">Decisões Pendentes</h3>
          <ul className="mt-3 space-y-2 text-sm">
            <li>Escalar mentoria premium para 3 capitais.</li>
            <li>Revisar política de orçamento acima de R$ 250k.</li>
            <li>Definir governança de novos canais de aquisição.</li>
          </ul>
        </article>
        <article className="panel p-5">
          <h3 className="font-semibold">Riscos Críticos</h3>
          <ul className="mt-3 space-y-2 text-sm">
            <li><span className="badge-risk-high">Alto</span> Inadimplência crescente em planos anuais.</li>
            <li><span className="badge-risk-medium">Médio</span> Atraso no onboarding de mentores.</li>
            <li><span className="badge-risk-medium">Médio</span> Concentração de receita em poucos canais.</li>
          </ul>
        </article>
      </div>
    </section>
  );
}

