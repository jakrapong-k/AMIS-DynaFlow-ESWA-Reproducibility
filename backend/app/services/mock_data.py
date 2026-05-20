from datetime import UTC, datetime

from app.models.entities import RunStatus


def now_utc() -> datetime:
    return datetime.now(UTC)


def sample_run_id() -> str:
    return f"run_{now_utc().strftime('%Y%m%d_%H%M%S')}"


def default_run_status() -> str:
    return RunStatus.QUEUED.value
