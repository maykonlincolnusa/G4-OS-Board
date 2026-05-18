from pydantic import BaseModel


class ServiceRecord(BaseModel):
    id: str
    tenant_id: str
    name: str

