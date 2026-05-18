INSERT INTO tenants (id, name, slug, plan)
VALUES
('11111111-1111-1111-1111-111111111111', 'NovaBoard Academy Group', 'novaboard', 'enterprise')
ON CONFLICT DO NOTHING;

INSERT INTO roles (key, label)
VALUES
('super_admin','Super Admin'),
('tenant_admin','Tenant Admin'),
('ceo','CEO'),
('board_member','Board Member'),
('founder','Founder'),
('cfo','CFO'),
('coo','COO'),
('cmo','CMO'),
('legal','Legal'),
('manager','Manager'),
('mentor','Mentor'),
('consultant','Consultant'),
('viewer','Viewer')
ON CONFLICT (key) DO NOTHING;

INSERT INTO permissions (key, description)
VALUES
('documents:read','Read documents'),
('kpi:read','Read KPIs'),
('decisions:create','Create decisions'),
('approvals:manage','Manage approvals'),
('agents:execute','Execute AI agents'),
('channels:read','Read connected channels'),
('financial:read','Read financial data'),
('legal:read','Read legal data'),
('boardpack:generate','Generate board packs'),
('audit:read','Read audit logs')
ON CONFLICT (key) DO NOTHING;

INSERT INTO users (id, tenant_id, email, full_name)
VALUES
('22222222-2222-2222-2222-222222222221','11111111-1111-1111-1111-111111111111','ceo@novaboard.ai','Ana Ribeiro'),
('22222222-2222-2222-2222-222222222222','11111111-1111-1111-1111-111111111111','cfo@novaboard.ai','Rafael Costa'),
('22222222-2222-2222-2222-222222222223','11111111-1111-1111-1111-111111111111','coo@novaboard.ai','Marina Lopes'),
('22222222-2222-2222-2222-222222222224','11111111-1111-1111-1111-111111111111','board@novaboard.ai','Carlos Menezes')
ON CONFLICT DO NOTHING;

INSERT INTO boards (id, tenant_id, name, cadence)
VALUES
('33333333-3333-3333-3333-333333333333','11111111-1111-1111-1111-111111111111','Conselho Estratégico','monthly')
ON CONFLICT DO NOTHING;

INSERT INTO meetings (id, tenant_id, board_id, title, starts_at, status)
VALUES
('44444444-4444-4444-4444-444444444441','11111111-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Board Meeting - Abril', NOW() - INTERVAL '20 days', 'completed'),
('44444444-4444-4444-4444-444444444442','11111111-1111-1111-1111-111111111111','33333333-3333-3333-3333-333333333333','Board Meeting - Maio', NOW() + INTERVAL '10 days', 'scheduled')
ON CONFLICT DO NOTHING;

INSERT INTO decisions (tenant_id, meeting_id, title, description, impact_level, risk_level, status)
VALUES
('11111111-1111-1111-1111-111111111111','44444444-4444-4444-4444-444444444441','Expandir programa de mentoria premium','Escalar mentoria premium para 3 novas capitais no próximo trimestre.','high','medium','open'),
('11111111-1111-1111-1111-111111111111','44444444-4444-4444-4444-444444444441','Revisar política de aprovação de orçamento','Adicionar dupla aprovação para contratos acima de R$ 250k.','high','high','in_progress');

INSERT INTO actions (tenant_id, title, status, priority, due_date)
VALUES
('11111111-1111-1111-1111-111111111111','Definir squad comercial para novas capitais','in_progress','high', CURRENT_DATE + 12),
('11111111-1111-1111-1111-111111111111','Atualizar workflow jurídico-financeiro','todo','high', CURRENT_DATE + 7),
('11111111-1111-1111-1111-111111111111','Publicar playbook de eventos enterprise','todo','medium', CURRENT_DATE + 21);

INSERT INTO risks (tenant_id, title, category, probability, impact, status)
VALUES
('11111111-1111-1111-1111-111111111111','Atraso no onboarding de mentores sêniores','operational',3,4,'open'),
('11111111-1111-1111-1111-111111111111','Aumento da inadimplência em planos anuais','financial',4,4,'open'),
('11111111-1111-1111-1111-111111111111','Dependência de poucos canais de aquisição','commercial',3,5,'monitoring');

INSERT INTO documents (id, tenant_id, title, category, area, access_level, content_text)
VALUES
('55555555-5555-5555-5555-555555555551','11111111-1111-1111-1111-111111111111','Ata de Reunião de Board - Abril','meeting_minutes','Board','board_only','Decisão de expansão da mentoria premium e reforço do comitê de risco.'),
('55555555-5555-5555-5555-555555555552','11111111-1111-1111-1111-111111111111','Relatório Comercial Q1','sales_report','Vendas','internal','Receita de R$ 8,4M no trimestre, conversão de 6,2%, CAC médio de R$ 1.240.'),
('55555555-5555-5555-5555-555555555553','11111111-1111-1111-1111-111111111111','Relatório Financeiro Mensal','finance_report','Financeiro','confidential','Margem EBITDA de 18,4%, inadimplência de 3,7%, caixa para 7,2 meses.'),
('55555555-5555-5555-5555-555555555554','11111111-1111-1111-1111-111111111111','Plano de Marketing Semestral','marketing_plan','Marketing','internal','Meta de crescimento de leads qualificados em 35% com foco em conteúdo e parcerias.'),
('55555555-5555-5555-5555-555555555555','11111111-1111-1111-1111-111111111111','Relatório de Customer Success','cs_report','Customer Success','internal','NPS médio de 71, churn mensal de 2,1%, 84 contas em risco moderado.'),
('55555555-5555-5555-5555-555555555556','11111111-1111-1111-1111-111111111111','Roadmap de Produto','product_roadmap','Produto','internal','Prioridades: board pack v2, alertas de risco e automação de aprovações.'),
('55555555-5555-5555-5555-555555555557','11111111-1111-1111-1111-111111111111','Matriz de Riscos Corporativos','risk_matrix','Jurídico','confidential','Riscos críticos: compliance de contratos, concentração de receita e execução operacional.'),
('55555555-5555-5555-5555-555555555558','11111111-1111-1111-1111-111111111111','Playbook de Vendas Enterprise','playbook','Vendas','internal','Processo de discovery, proposta, negociação e fechamento enterprise em 6 etapas.'),
('55555555-5555-5555-5555-555555555559','11111111-1111-1111-1111-111111111111','Playbook de Eventos','playbook','Eventos','internal','Checklist operacional para eventos com 500+ executivos e sponsors.'),
('55555555-5555-5555-5555-55555555555a','11111111-1111-1111-1111-111111111111','Política de Aprovação de Orçamento','policy','Financeiro','board_only','Toda despesa acima de R$ 250 mil exige aprovação Financeiro + COO + Board.');

INSERT INTO kpis (tenant_id, area, metric_key, metric_label, value, period)
VALUES
('11111111-1111-1111-1111-111111111111','Financeiro','monthly_revenue','Receita Mensal',2950000,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Marketing','leads','Leads',18200,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Vendas','conversion_rate','Conversão (%)',6.2,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Marketing','cac','CAC',1240,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Financeiro','ltv','LTV',14500,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Customer Success','churn','Churn (%)',2.1,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Customer Success','nps','NPS',71,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Cursos','active_students','Alunos Ativos',9340,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Eventos','event_participation','Participação em Eventos',76,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Financeiro','default_rate','Inadimplência (%)',3.7,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Financeiro','margin','Margem (%)',18.4,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Operações','avg_resolution_time','Tempo Médio de Resolução (h)',19,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Operações','overdue_actions','Ações Atrasadas',14,CURRENT_DATE),
('11111111-1111-1111-1111-111111111111','Risco','open_risks','Riscos Abertos',23,CURRENT_DATE);

