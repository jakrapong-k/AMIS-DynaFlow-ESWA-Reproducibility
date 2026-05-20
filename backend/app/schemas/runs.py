from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CreateRunRequest(BaseModel):
    run_type: str
    input_ref: str | None = None
    config: dict[str, Any]


class CreateRunResponse(BaseModel):
    run_id: str
    status: str
    created_at: datetime


class RunSummary(BaseModel):
    run_id: str
    run_type: str
    status: str
    created_by: str
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class RunListResponse(BaseModel):
    items: list[RunSummary]
    total: int


class RunDetailResponse(BaseModel):
    run_id: str
    status: str
    status_message: str
    run_type: str
    config_hash: str
    input_hash: str
    created_by: str
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: str | None = None


class MetricItem(BaseModel):
    name: str
    value: float


class RunMetricsResponse(BaseModel):
    run_id: str
    metrics: list[MetricItem]


class ArtifactItem(BaseModel):
    type: str
    path: str
    checksum: str


class RunArtifactsResponse(BaseModel):
    run_id: str
    artifacts: list[ArtifactItem]
