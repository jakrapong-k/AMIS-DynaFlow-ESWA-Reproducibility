from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException

from app.schemas.runs import (
    ArtifactItem,
    CreateRunRequest,
    CreateRunResponse,
    MetricItem,
    RunArtifactsResponse,
    RunDetailResponse,
    RunListResponse,
    RunMetricsResponse,
    RunSummary,
)
from app.services.mock_data import default_run_status, sample_run_id

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("", response_model=CreateRunResponse, status_code=202)
def create_run(_: CreateRunRequest) -> CreateRunResponse:
    return CreateRunResponse(
        run_id=sample_run_id(),
        status=default_run_status(),
        created_at=datetime.now(UTC),
    )


@router.get("", response_model=RunListResponse)
def list_runs(status: str | None = None, limit: int = 20, offset: int = 0) -> RunListResponse:
    _ = (status, limit, offset)
    return RunListResponse(items=[], total=0)


@router.get("/{run_id}", response_model=RunDetailResponse)
def get_run(run_id: str) -> RunDetailResponse:
    if not run_id.startswith("run_"):
        raise HTTPException(status_code=404, detail="Run id not found")

    return RunDetailResponse(
        run_id=run_id,
        status="succeeded",
        status_message="completed",
        run_type="full_pipeline",
        config_hash="sha256:placeholder",
        input_hash="sha256:placeholder",
        created_by="usr_mock_001",
        created_at=datetime.now(UTC),
        started_at=datetime.now(UTC),
        finished_at=datetime.now(UTC),
        error=None,
    )


@router.get("/{run_id}/metrics", response_model=RunMetricsResponse)
def get_run_metrics(run_id: str) -> RunMetricsResponse:
    return RunMetricsResponse(
        run_id=run_id,
        metrics=[
            MetricItem(name="mae", value=2.31),
            MetricItem(name="service_level", value=0.94),
            MetricItem(name="utilization", value=0.88),
        ],
    )


@router.get("/{run_id}/artifacts", response_model=RunArtifactsResponse)
def get_run_artifacts(run_id: str) -> RunArtifactsResponse:
    return RunArtifactsResponse(
        run_id=run_id,
        artifacts=[
            ArtifactItem(
                type="summary_csv",
                path="results/sample_outputs/reproduction_summary.csv",
                checksum="sha256:placeholder",
            )
        ],
    )
