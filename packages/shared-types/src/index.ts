export type TenantScope = {
  tenantId: string;
  workspace?: string;
};

export type ActorContext = {
  userId: string;
  role: string;
};

export type AuditEnvelope = {
  requestId: string;
  correlationId: string;
  tenantId: string;
};

