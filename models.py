from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ConfigCreateRequest(BaseModel):
    data: dict[str, Any] = Field(..., description='Key-value configuration data')
    created_by: str


class ConfigResponse(BaseModel):
    service: str
    environment: str
    version: str
    data: dict[str, Any]
    created_at: datetime
    created_by: str
