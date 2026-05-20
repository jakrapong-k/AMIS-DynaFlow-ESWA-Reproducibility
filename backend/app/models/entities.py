from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any


class UserRole(StrEnum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class RunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


ALLOWED_STATUS_TRANSITIONS: dict[RunStatus, set[RunStatus]] = {
    RunStatus.QUEUED: {RunStatus.RUNNING, RunStatus.CANCELLED},
    RunStatus.RUNNING: {RunStatus.SUCCEEDED, RunStatus.FAILED, RunStatus.CANCELLED},
    RunStatus.SUCCEEDED: set(),
    RunStatus.FAILED: set(),
    RunStatus.CANCELLED: set(),
}


@dataclass
class User:
    id: str
    email: str
    password_hash: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class Run:
    id: str
    created_by: str
    run_type: str
    status: RunStatus
    status_message: str | None
    input_ref: str | None
    input_hash: str | None
    config_json: dict[str, Any]
    config_hash: str | None
    seed: int | None
    error_code: str | None
    error_detail: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None


@dataclass
class RunMetric:
    id: int
    run_id: str
    metric_name: str
    metric_value: float
    metric_group: str | None
    created_at: datetime


@dataclass
class Artifact:
    id: int
    run_id: str
    artifact_type: str
    path_or_uri: str
    checksum: str | None
    size_bytes: int | None
    created_at: datetime


@dataclass
class AuditLog:
    id: int
    user_id: str | None
    action: str
    resource_type: str
    resource_id: str | None
    metadata_json: dict[str, Any] | None
    created_at: datetime


def can_transition(from_status: RunStatus, to_status: RunStatus) -> bool:
    return to_status in ALLOWED_STATUS_TRANSITIONS[from_status]
