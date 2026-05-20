from fastapi import APIRouter

from app.schemas.dashboard import DashboardSummaryResponse, DashboardTrendsResponse, DailyTrendItem

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary() -> DashboardSummaryResponse:
    return DashboardSummaryResponse(
        total_runs=0,
        success_rate=0.0,
        avg_runtime_seconds=0,
        active_runs=0,
    )


@router.get("/trends", response_model=DashboardTrendsResponse)
def dashboard_trends() -> DashboardTrendsResponse:
    return DashboardTrendsResponse(
        daily=[DailyTrendItem(date="2026-05-19", runs=0, success_rate=0.0)]
    )
